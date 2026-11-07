# DevOps half — runbook

**Budget:** about 22 minutes of demonstration inside a 45-minute block.

Infrastructure that worked yesterday is broken this morning. Nobody watched it
happen. An agent with read-only access to the account finds the change, names
the person — or the pipeline — that made it, and proposes the fix.

> ⚠️ **Rehearse this once before delivering it.** The pieces are verified
> individually (see *What has been checked*, at the end) but the full sequence
> with the break applied has not yet been run end to end. The agent's exact
> output is not predictable the way the first half's is.

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
curl -s -o /dev/null -w '%{http_code}\n' https://status.awsf.brightkey.cloud/   # expect 503
```

**Leave at least 30 minutes between the merge and the session.** CloudTrail and
AWS Config both need time to record. Config discovered this account's security
group within about two minutes of creation, so minutes rather than hours — but
do not cut it fine.

### Checklist

- [ ] Stack deployed, application deployed, board seeded
- [ ] Breaking change merged, pipeline applied it, board returns 503
- [ ] At least 30 minutes elapsed since the merge
- [ ] AWS MCP connected **as the read-only agent role** (see below)
- [ ] GitHub MCP still connected from the first half
- [ ] The intended-state diagram open in a tab, ready to show
- [ ] A browser tab signed in to GitHub

### Connecting the AWS MCP as the read-only role

The agent must not be able to fix anything. Add a profile that assumes the
read-only role:

```ini
# ~/.aws/config
[profile status-board-agent]
role_arn       = arn:aws:iam::997075698610:role/demo-status-board-agent
source_profile = default
region         = us-east-1
```

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

Load the board. It returns 503.

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

What to expect it to do, roughly in order: check the load balancer's target
health and find the target failing, look at the task security group, query
AWS Config for that group's configuration history to get the before and after,
then search CloudTrail for the API call that changed it.

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

Once the agent has the CloudTrail event, it has a timestamp and an identity —
an assumed role, not a person. Ask it to close the loop:

> Which pull request caused this?

It reaches GitHub through the MCP connected in the first half, finds the merge
that fired the pipeline, and names the change.

Two MCP servers, one question. Neither could answer it alone: AWS knows what
happened and when, GitHub knows why and who decided it. The agent is the only
thing holding both.

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
| The agent reaches the answer in 30 seconds | Good. Spend the time saved on the correlation step, which is the part worth dwelling on |
| Copilot review is slow on the revert | Request it, then run the discussion while it arrives |

## What has been checked

Verified on 2026-11-07 against the live account:

- **The AWS MCP can run Config advanced queries.** `SelectResourceConfig`
  returns the task security group and its `ipPermissions`, including the
  ingress rule's description.
- **Config records promptly here.** The security group was discovered about two
  minutes after creation, with four configuration items inside five minutes.
  Recording is continuous and account-wide, enabled since 2019.
- **The agent role is genuinely read-only.** Reads of CloudTrail, Config, EC2
  and ECS succeed; `RevokeSecurityGroupIngress` and
  `AuthorizeSecurityGroupIngress` against a real security group both fail with
  "explicit deny in an identity-based policy".
- **The breaking change is staged** as
  [status-board-infra#1](https://github.com/brightkeycloud-chad/status-board-infra/pull/1)
  and `terraform validate` passes. It removes exactly one resource.

Not yet observed, and the reason to rehearse: the CloudTrail event the pipeline
produces when it applies the removal, the before-and-after pair Config captures
for it, and how long the board takes to start returning 503.
