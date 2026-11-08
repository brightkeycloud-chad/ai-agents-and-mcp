# Environment — provision and teardown

**The infrastructure and the application must be up before any demonstration
starts, including the development half.** Tear them down when you are finished.

Run this on its own, separately from the demonstrations. If an agent is doing
it, use a dedicated conversation that only provisions or tears down.

**Allow about 10 minutes** to bring it up. The stack costs about **$0.10 per
hour** while it exists.

> The workflows and the check commands are the ones the course already uses.
> The `run_and_wait` helper below is new and has not yet been run against a real
> workflow. Remove this note after the first bring-up succeeds.

## What this covers

| In scope | Out of scope |
|---|---|
| The stack in `status-board-infra/terraform` | `bootstrap/`, which stays live between deliveries |
| Deploying the application and seeding the board | The breaking change, which belongs to the [DevOps half](../02-devops/RUNBOOK.md) |
| Tearing the stack down, and confirming it has gone | Everything else in the account |

**The account holds resources from other courses.** Do not touch anything whose
name does not contain `status-board`.

## Before you start

Check that the foundations are still there. None of this should need creating:

```bash
aws sts get-caller-identity --query Account --output text   # expect 997075698610
gh auth status

aws iam list-roles \
  --query "Roles[?starts_with(RoleName,'demo-status-board')].RoleName" --output text
# expect demo-status-board-agent, -app-deploy and -tf-deploy

aws s3api head-bucket --bucket demo-status-board-tfstate-997075698610   # expect no error
```

If a role or the bucket is missing, stop. The foundations have been removed, and
rebuilding them is a separate job covered in the
[`status-board-infra` README](https://github.com/brightkeycloud-chad/status-board-infra#bringing-it-up).

Then check that `main` still has the ingress rule the board depends on. If the
breaking change is merged, a new stack comes up broken:

```bash
gh api repos/brightkeycloud-chad/status-board-infra/contents/terraform/security_groups.tf \
  -H 'Accept: application/vnd.github.raw' | grep -c task_from_alb   # expect 1 or more
```

## Define the helper

`gh workflow run` returns before the run exists, so looking up "the latest run"
straight afterwards can return the previous one, which has already finished.
This helper waits for a new run ID, then follows that run to the end. Paste it
once per shell:

```bash
INFRA=brightkeycloud-chad/status-board-infra
APP=brightkeycloud-chad/status-board-app

latest_run() {
  gh run list --repo "$1" --workflow "$2" --limit 1 \
    --json databaseId --jq '.[0].databaseId'
}

# Usage: run_and_wait <repo> <workflow> [gh workflow run options]
run_and_wait() {
  local repo=$1 workflow=$2 before run
  shift 2
  before=$(latest_run "$repo" "$workflow")
  gh workflow run "$workflow" --repo "$repo" "$@" || return 1
  run=$before
  until [ -n "$run" ] && [ "$run" != "$before" ]; do
    sleep 3
    run=$(latest_run "$repo" "$workflow")
  done
  echo "following run $run"
  gh run watch "$run" --repo "$repo" --exit-status
}
```

## Bring it up

Run these in order. Each must succeed before the next starts, because the
application deployment needs the ECR repository and the ECS service that the
first step creates.

```bash
# 1. The stack. About 4 minutes.
run_and_wait "$INFRA" terraform.yml

# 2. The application and the seed data. About 3 minutes.
run_and_wait "$APP" deploy.yml
```

Until step 2 finishes, the ECS service restarts repeatedly because it has no
image to pull. That is expected on a fresh build.

### Confirm it works

The deployment already checks the board before it reports success. Check again
from your own machine:

```bash
curl -s -o /dev/null -w '%{http_code}\n' https://status.awsf.brightkey.cloud/healthz
# expect 200

curl -s https://status.awsf.brightkey.cloud/api/services \
  | python3 -c 'import json,sys; print(len(json.load(sys.stdin)))'
# expect 4 or more
```

Then open <https://status.awsf.brightkey.cloud> and confirm the board renders.

**The environment is ready when both checks pass and the board renders.** Do not
start a demonstration before then.

## Tear it down

Do this after every rehearsal and every delivery. The workflow refuses to run
unless the confirmation is exactly `destroy`.

```bash
run_and_wait "$INFRA" destroy.yml -f confirm=destroy
```

### Confirm it has gone

```bash
aws ecs list-clusters --query "clusterArns[?contains(@,'status-board')]" --output text
aws elbv2 describe-load-balancers \
  --query "LoadBalancers[?contains(LoadBalancerName,'status-board')].LoadBalancerName" --output text
aws dynamodb list-tables --query "TableNames[?contains(@,'status-board')]" --output text
aws ecr describe-repositories \
  --query "repositories[?contains(repositoryName,'status-board')].repositoryName" --output text
# expect all four to print nothing

# The Terraform name for the gateway contains status-board.
aws ec2 describe-nat-gateways \
  --filter Name=state,Values=available,pending "Name=tag:Name,Values=*status-board*" \
  --query "NatGateways[].NatGatewayId" --output text
# expect nothing
```

The destroy workflow's summary also lists what remains, but its NAT gateway list
covers the whole account, so a gateway there may belong to something else.

**These stay on purpose**, and cost little or nothing: the OIDC provider, the
three `demo-status-board-*` roles and the state bucket.

## Things that can go wrong

| Problem | What to do |
|---|---|
| The application deployment fails at the ECR login or push | The stack is not finished, or it failed. Check the `terraform` run, then run step 2 again |
| The board returns 504 straight after a bring-up | The breaking change is probably on `main`. Run the ingress rule check above. Do not fix it from here if a DevOps rehearsal is in progress |
| The board returns 503 | The task is not healthy yet, or it has no image. Check that step 2 finished, and look at the ECS service events |
| `/healthz` returns 200 but there are fewer than 4 services | The seed step did not complete. Run step 2 again; seeding is safe to repeat |
| A run waits at `queued` for a long time | Another `terraform` or `destroy` run holds the concurrency group. They queue rather than overlap, so let the first one finish |
| Terraform reports a state lock | A run was interrupted. Confirm no run is active in the Actions tab before doing anything about the lock |
| Teardown fails partway | Run it again, then repeat the checks. If it still fails, look at what remains before deleting anything by hand |
