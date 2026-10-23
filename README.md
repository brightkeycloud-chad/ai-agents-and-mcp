# AI Agents and MCP in Development and Operations

Course material for the Pearson live training of the same name. Two hours,
split evenly between software development and DevOps, built on one application
and one AWS account throughout.

This repository holds the **documentation**: runbooks, diagrams, and the
reference copies of anything built live. The code and the infrastructure live
in their own repositories.

| Repository | Holds |
|---|---|
| [`status-board-app`](https://github.com/brightkeycloud-chad/status-board-app) | The Service Status Board application, and its deployment workflow |
| [`status-board-infra`](https://github.com/brightkeycloud-chad/status-board-infra) | The AWS infrastructure that runs it, and its Terraform workflows |
| **this repository** | Runbooks, diagrams, and course documentation |

## The demonstrations

| | What happens | Status |
|---|---|---|
| [Development](demos/01-development/RUNBOOK.md) | Build a scoped, read-only review agent and point it at a real pull request, then ask GitHub Copilot to review the same one | Ready |
| DevOps | Infrastructure that worked yesterday is broken. An agent investigates with CloudTrail and AWS Config, correlates the change to a merged pull request, and proposes a revert | Being built |

Both halves use the same system, so the second half investigates an
application the audience has already read the code for.

## The shape of it

A small FastAPI board showing the health of four services, running on ECS
Fargate behind an HTTPS load balancer, storing state in two DynamoDB tables.
Deployed by GitHub Actions through OIDC, with no access key anywhere.

Architecture diagrams live with the code they describe, and each component
cites the line that proves it:

- [Infrastructure](https://github.com/brightkeycloud-chad/status-board-infra/blob/main/docs/architecture.png)
- [Application](https://github.com/brightkeycloud-chad/status-board-app/blob/main/docs/architecture.png)

## Sources

Every third-party reference behind this material, with what it establishes and
when it was checked, is in [SOURCES.md](SOURCES.md). It also lists the two
claims that have **not** been verified, and the facts that have already changed
once — read it before putting a number on a slide.

## Running a demonstration

Each runbook lists its own prerequisites, timings, reset steps and failure
modes. Read it before the session, not during one.

**The development half needs no AWS resources.** The DevOps half does, and the
stack costs about **$0.10 per hour** while it exists. Bring it up before a
rehearsal and tear it down afterwards:

```bash
# in status-board-infra
cd terraform && terraform apply        # or run the terraform workflow
# ... and afterwards, the destroy workflow, or:
cd terraform && terraform destroy
```

## What this course is not

It is not a tour of products. The tools in it will have changed by the time you
need them. What should outlast them is the three ideas underneath: scope the
tools an agent can reach, count the context every connected tool costs, and
keep a person in the path that approves a change.

---

The previous version of this course is preserved in
[`old_course_version/`](old_course_version/). It covered Kiro and Amazon Q
Developer, both of which this version drops.
