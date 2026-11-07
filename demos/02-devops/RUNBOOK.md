# DevOps half — runbook

**Budget:** about 22 minutes of demonstration inside a 45-minute block.

Infrastructure that worked yesterday is broken this morning. Nobody watched it
happen. An agent with read-only access to the account finds the change, names
the person — or the pipeline — that made it, and proposes the fix.

> The break has been run end to end against the live account. Everything below
> that describes what the evidence looks like is observed, not expected — see
> *What has been checked* at the end for the measurements.

## Before the session

This half depends on evidence that only accumulates with time, so most of the
work happens before anyone is watching.

### The day before, or at least an hour ahead

```bash
# 1. Bring the stack up. About 4 minutes.
gh workflow run terraform.yml --repo brightkeycloud-chad/status-board-infra

# 2. Deploy the application and seed the board. About 3 minutes.
gh workflow run deploy.yml --repo brightkeycloud-chad/status-board-app

# 3. Confirm the board is healthy before you break it.
curl -s -o /dev/null -w '%{http_code}\n' https://status.awsf.brightkey.cloud/healthz   # expect 200
```

Then **merge the breaking change and let the pipeline apply it**:

```bash
gh pr merge 1 --repo brightkeycloud-chad/status-board-infra --squash
```

That matters more than it looks. A human running `terraform apply` puts their
own identity in CloudTrail. Merging makes the **pipeline** apply it, so
CloudTrail records an assumed role — which is the better story: the change was
authorised, applied correctly by automation, and still wrong.

Wait for the apply to finish, then confirm the break took:

```bash
curl -s -m 30 -o /dev/null -w '%{http_code}\n' https://status.awsf.brightkey.cloud/   # expect 504
```

**The evidence lands faster than you would think.** Measured end to end: the
CloudTrail event appeared **30 seconds** after the merge, the board began
failing at **40 seconds**, AWS Config captured the change at **74 seconds**,
and the event was queryable through `LookupEvents` within about **90 seconds**.

So five minutes is operationally enough. Leave longer anyway — half an hour,
or do it the night before — because the story is that the evidence is cold by
the time anyone arrives, and a timestamp two minutes old undercuts it.

### Checklist

- [ ] Stack deployed, application deployed, board seeded
- [ ] Breaking change merged, pipeline applied it, board returns 503
- [ ] At least 30 minutes elapsed since the merge
- [ ] AWS MCP connected **as the read-only agent role** (profile already configured; see below)
- [ ] GitHub MCP still connected from the first half
- [ ] The intended-state diagram open in a tab, ready to show
- [ ] A browser tab signed in to GitHub

### Connecting the AWS MCP as the read-only role

The agent must not be able to fix anything. The profile is already in
`~/.aws/config` on the demonstration machine:

```ini
[profile status-board-agent]
role_arn       = arn:aws:iam::997075698610:role/demo-status-board-agent
source_profile = default
region         = us-east-1
output         = json
```

The role's maximum session is one hour, which is shorter than the course. That
is fine: with `role_arn` and `source_profile` the CLI and SDK re-assume
automatically, so a two-hour session does not need handling.

Check it is scoped as intended before the session:

```bash
AWS_PROFILE=status-board-agent aws sts get-caller-identity          # assumed-role/demo-status-board-agent
AWS_PROFILE=status-board-agent aws ec2 describe-security-groups --max-items 1 >/dev/null && echo "read: ok"
AWS_PROFILE=status-board-agent aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxx --protocol tcp --port 8080 --cidr 10.0.0.0/8      # expect an explicit deny
```

That last command should fail with **"with an explicit deny in an
identity-based policy"**. Keep it in your scrollback — it is worth showing.

## Running it

### 1. Add the AWS MCP server alongside GitHub — 3 min

Two servers now, and no more. Say the number out loud.

Point out that the agent is being given **read-only credentials**, and show the
explicit denial from the checklist above. Scoping an agent is not a precaution
bolted on afterwards; it is the first decision you make about it.

### 2. Show the intended state — 2 min

Open the committed diagram:
[`status-board-infra/docs/architecture.html`](https://github.com/brightkeycloud-chad/status-board-infra/blob/main/docs/architecture.html)

Walk the request path once: Route 53, the load balancer in public subnets, the
Fargate task in private subnets, DynamoDB behind it. Name the two security
group boundaries.

**Do not show a broken version, and do not highlight what is about to fail.**
The audience should see only how it is supposed to work. The diagram is
committed to the repository, so the agent can read it as context too.

### 3. The symptom — 2 min

Load the board. **It hangs for about ten seconds, then returns 504.**

Let the hang play out on screen rather than cutting away — the pause is the
most visceral part of the whole half, and it tells you something a 503 would
not. A 503 means the load balancer has nothing to send the request to. A 504
means it found a target, forwarded the request, and waited. Something is
swallowing packets rather than refusing them, which is what a security group
does.

Set the scene honestly: the environment worked yesterday, a change merged
overnight, nobody saw it happen, and the evidence is already cold. That is what
every real investigation looks like.

**Say that the merge happened before the session.** Someone will notice the
timestamp, and it is better coming from you.

### 4. The agent investigates — 8 min

Give it the symptom, not the answer:

> The status board at https://status.awsf.brightkey.cloud is returning 503. It
> was working yesterday. Use CloudTrail and AWS Config to work out what
> changed, when, and who changed it. You have read-only access.

What it finds, in roughly this order. All of it is real output from the run on
2026-11-07:

**Target health** names the failure mode:

```
state  unhealthy    reason  Target.Timeout    "Request timed out"
```

**Do not script that reason string.** ECS keeps replacing the task it cannot
reach, so depending on where in that cycle you look it may read
`Target.DeregistrationInProgress` or `Target.Timeout`. Both were observed
within minutes of each other. What is stable is `state: unhealthy` — say that,
and read whatever reason is on screen.

**AWS Config** gives a clean before and after on the same resource:

```
23:15:45   ingress rules: 0   ports: []        ← after
22:16:13   ingress rules: 1   ports: [8080]    ← before
```

**CloudTrail** names the call and who made it:

```
eventTime      2026-11-07T23:15:01Z
eventName      RevokeSecurityGroupIngress
userIdentity   AssumedRole
arn            .../demo-status-board-tf-deploy/gha-terraform-42424330726
userAgent      APN/1.0 HashiCorp/1.0 Terraform/1.17.1
groupId        sg-03a5ad45163aec881
```

Pause on that `userIdentity`. It is an **assumed role, not a person**, and the
user agent says Terraform. Nobody logged into the console and clicked
something. The change was authorised, applied correctly by automation, and
still wrong — which is the uncomfortable kind of incident, and the common
kind.

The Config query it is reaching for looks like this, and works through the AWS
MCP:

```sql
SELECT resourceId, resourceName, configuration.ipPermissions
WHERE resourceType = 'AWS::EC2::SecurityGroup'
  AND resourceName = 'demo-status-board-task-sg'
```

**Let it work.** Narrate what it is doing rather than filling the silence. If
it stalls, nudge with the symptom rather than the cause — "what does the load
balancer think of its target?" is fair; "look at the security group" is not.

### 5. The correlation — 3 min

This is the high point of the half. Build toward it.

Look again at the role session name in the CloudTrail event:

```
arn:aws:sts::997075698610:assumed-role/demo-status-board-tf-deploy/gha-terraform-42424330726
                                                                   └──────────┬──────────┘
                                                                   the GitHub Actions run id
```

The workflow sets `role-session-name: gha-terraform-${{ github.run_id }}`, so
**AWS is carrying GitHub's run id inside the identity that made the change.**
This is not timestamp matching. It is an exact key.

Ask the agent to follow it:

> Which pull request caused this?

It reaches GitHub through the MCP connected in the first half, and the chain
resolves without ambiguity:

```
CloudTrail session   gha-terraform-42424330726
         ↓
Actions run          42424330726
         ↓
commit               7cfcd61
         ↓
pull request         #1  "Remove redundant task security group ingress rule"
```

Then read the pull request body out loud. Its argument is that the rule is
redundant because the load balancer already has a matching egress rule. That
is a real misreading of how security groups work — egress on the source does
not grant ingress on the destination — and it is plausible enough that it got
merged.

Two MCP servers, one question. Neither could answer it alone: AWS knows what
happened and when, GitHub knows why and who decided it. The agent is the only
thing holding both.

**Worth saying:** that session name was set for traceability, not for this. A
small, cheap convention in a workflow turned a correlation problem into a
lookup. Those conventions are worth paying for before you need them.

### 6. Propose the fix, and let Copilot review it — 4 min

> Open a pull request that restores the rule.

The agent cannot apply it — its role denies every write — so the only thing it
can do is propose. A person still approves and merges. That is the point, not
a limitation.

Then request a **Copilot review on the agent's pull request**, which closes the
loop with the first half: the same reviewer, now reviewing an agent's work
rather than a human's.

Show the after-the-fix diagram if you have it, or simply re-run the request and
watch the board come back.

### 7. Discussion

> **Use MCPs and agents, or just let the model figure it out?**

Worth having an answer ready. The model alone could have told you what a 503
behind a load balancer usually means. What it could not do is tell you that
*this* security group changed at *that* minute because of *that* pull request.
The MCP servers are not making the model smarter; they are giving it facts
about your account that it could not otherwise have.

And the counterweight: two servers was a decision. Seven would have cost
context on every turn and given the agent more ways to pick the wrong tool.

## Resetting between runs

```bash
# Put the rule back and rebuild, or tear down entirely.
cd status-board-infra
git checkout main && git revert --no-edit <the-merge-sha>   # or re-open the PR
gh workflow run terraform.yml --repo brightkeycloud-chad/status-board-infra

# Finished for the day — stop the billing.
gh workflow run destroy.yml --repo brightkeycloud-chad/status-board-infra -f confirm=destroy
```

Close any pull request the agent opened, and dismiss the Copilot review on it.

**The stack costs about $0.10 an hour while it exists.** Destroy it after every
rehearsal.

## Things that can go wrong

| Problem | What to do |
|---|---|
| The agent cannot find the CloudTrail event | Check how long ago the merge was. LookupEvents is not instant; 30 minutes is the floor |
| Config returns nothing for the security group | Confirm the recorder is on: `aws configservice describe-configuration-recorder-status`. This account records continuously |
| The agent tries to fix it and fails | That is the demonstration working. Show the explicit denial and move on |
| The board comes back by itself | It will not — the rule is gone until something restores it. If it does, the merge did not apply; check the workflow run |
| The board returns 503 rather than 504 | The task has been deregistered, probably because ECS replaced it. Still a valid symptom, but target health reads `no healthy targets` rather than `Target.Timeout` |
| The agent reaches the answer in 30 seconds | Good. Spend the time saved on the correlation step, which is the part worth dwelling on |
| Copilot review is slow on the revert | Request it, then run the discussion while it arrives |

## What has been checked

Run end to end against the live account on 2026-11-07. Measured from the merge:

| | Elapsed |
|---|---|
| CloudTrail recorded `RevokeSecurityGroupIngress` | **30s** |
| Board began failing | **40s** |
| Pipeline finished | **65s** |
| AWS Config captured the new configuration | **74s** |
| CloudTrail event queryable via `LookupEvents` | **~90s** |

Also confirmed:

- **The AWS MCP can run Config advanced queries**, and `GetResourceConfigHistory`
  returns a clean before-and-after pair for the security group.
- **CloudTrail records an assumed role**, not a person, with a Terraform user
  agent — because the pipeline applied the change.
- **The role session name carries the GitHub Actions run id**, which resolves
  to the run, the commit and the pull request with no guessing.
- **The agent role is genuinely read-only.** `RevokeSecurityGroupIngress` and
  `AuthorizeSecurityGroupIngress` against a real security group both fail with
  "explicit deny in an identity-based policy".
- **The failure mode is 504 after a ten-second hang**, with target health
  reading `Target.Timeout`. Not the 503 an earlier draft of this runbook
  predicted.

Still unobserved: the agent's own investigation of this evidence, end to end,
and the Copilot review of the revert. Both are worth one rehearsal.
