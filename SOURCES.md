# Third-party sources

Every external reference used while building this course, with what it
established and when it was checked.

**Why this file exists.** Claims on a slide need a source behind them, and
several facts here contradict what was true a year ago. Re-check anything
load-bearing in the week of delivery — the section at the end lists what has
already changed once.

---

## GitHub Copilot code review

| Source | Establishes | Checked |
|---|---|---|
| <https://docs.github.com/en/copilot/concepts/agents/code-review> | Copilot "reviews your code written in any language" — there is **no fixed language list**. Billing is AI-credit based: Lite $0.05–$1, Balanced $0.25–$5 per review. Automatic reviews bill the pull request author; manual reviews bill the requester. Included in Pro, Pro+, Business, Enterprise and Max; not in Free. | 2026-09-17 |
| <https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/configure-coding-guidelines> | Copilot code review **reads repository custom instructions by default**, including `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, and agent instructions in `AGENTS.md`, `CLAUDE.md` or `GEMINI.md` — taken from the **head branch**. Nothing indicates it can read files outside the pull request beyond those instruction files. | 2026-09-17 |

Both matter for the development half. The comparison is **not** that one
reviewer knows the house rules and the other does not — they both read
`AGENTS.md`. It is that one can open a file the pull request never touched.

## Terraform and the AWS provider

| Source | Establishes | Checked |
|---|---|---|
| <https://registry.terraform.io/v1/providers/hashicorp/aws> | Latest published provider version. Was `6.66.0`, published 2026-09-21. | 2026-09-21 |
| <https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/nat_gateway.html.markdown> | `aws_nat_gateway` supports `availability_mode` with values `zonal` (default) and `regional`. `subnet_id` must **not** be set when regional; use `vpc_id`. | 2026-09-21 |
| <https://github.com/hashicorp/terraform-provider-aws/issues/45828> | Open bug: a regional NAT gateway with **explicitly declared** `availability_zone_address` blocks fails on destroy ordering when the zone count changes. Avoided by leaving the gateway in automatic mode. | 2026-09-21 |
| <https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/r/ecs_service.html.markdown> | `availability_zone_rebalancing` accepts `ENABLED` / `DISABLED`, and defaults to enabled on a new compatible service. | 2026-09-26 |

## AWS documentation

| Source | Establishes | Checked |
|---|---|---|
| <https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html> | A regional NAT gateway is one gateway spanning the Availability Zones. It needs **no public subnet of its own**, auto-expands as workloads appear in new zones, and AWS creates its route table pre-wired to the internet gateway. | 2026-09-21 |
| <https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-amazon-vpc-regional-nat-gateway/> | Background on the regional availability mode and why it exists. | 2026-09-21 |
| <https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_AvailabilityZoneAddress.html> | The per-zone Elastic IP configuration for regional NAT gateways. Omitting it keeps auto-expansion on. | 2026-09-21 |
| <https://docs.aws.amazon.com/elasticloadbalancing/latest/APIReference/API_ModifyTargetGroup.html> | Target group health check limits: interval **5–300s**, timeout **2–120s**, and `HealthyThresholdCount` **minimum 2** — one is not permitted on an Application Load Balancer. | 2026-09-26 |
| <https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ql-iam.html> | PartiQL is authorised by its **own IAM actions** — `dynamodb:PartiQLSelect`, `PartiQLInsert`, `PartiQLUpdate`, `PartiQLDelete` — not by `GetItem`, `PutItem`, `UpdateItem` or `Query`. | 2026-10-17 |

That last one is the closing beat of the development half: the planted pull
request would fail with `AccessDenied` in AWS while every test passed.

## GitHub Actions runners

| Source | Establishes | Checked |
|---|---|---|
| <https://github.blog/changelog/2026-01-29-arm64-standard-runners-are-now-available-in-private-repositories/> | arm64 standard runners became generally available in **private** repositories in January 2026, free-tier eligible, with 2 vCPUs in private repos and 4 in public. | 2026-09-26 |
| <https://github.blog/changelog/2025-08-07-arm64-hosted-runners-for-public-repositories-are-now-generally-available/> | The earlier public-repository general availability, for timeline context. | 2026-09-26 |
| <https://docs.github.com/en/actions/reference/runners/github-hosted-runners> | Runner labels and specifications, including `ubuntu-24.04-arm`. | 2026-09-26 |

## Action versions

Each confirmed from its latest GitHub release. **Several are majors ahead of
where habit would put them** — worth re-checking before delivery.

| Action | Version | Checked |
|---|---|---|
| `actions/checkout` | v7 | 2026-09-26 |
| `actions/setup-python` | v7 | 2026-09-26 |
| `aws-actions/configure-aws-credentials` | **v6** | 2026-09-26 |
| `aws-actions/amazon-ecr-login` | v2 | 2026-09-26 |
| `aws-actions/amazon-ecs-render-task-definition` | v1 | 2026-09-26 |
| `aws-actions/amazon-ecs-deploy-task-definition` | v2 | 2026-09-26 |
| `docker/setup-qemu-action` | v4 | 2026-09-26 |
| `docker/setup-buildx-action` | v4 | 2026-09-26 |
| `docker/build-push-action` | v7 | 2026-09-26 |
| `hashicorp/setup-terraform` | v4 | 2026-09-26 |

<https://raw.githubusercontent.com/aws-actions/configure-aws-credentials/v6/action.yml>
confirms v6 keeps the `role-to-assume`, `aws-region` and `role-session-name`
input names, so the major bump needs no migration. Checked 2026-09-26.

## Claude Code

| Source | Establishes | Checked |
|---|---|---|
| <https://code.claude.com/docs/en/sub-agents> | Subagent file format. Required frontmatter is `name` and `description`; `tools` is a comma-separated string or YAML list; project agents live in `.claude/agents/`, user agents in `~/.claude/agents/`. A **restart is required only when creating the first agent file in a new `agents/` directory** — later edits are picked up within seconds. | 2026-10-12 |

## GitHub MCP server

| Source | Establishes | Checked |
|---|---|---|
| <https://raw.githubusercontent.com/github/github-mcp-server/main/README.md> | The full toolset list. Defaults when none are specified: `context, repos, issues, pull_requests, users`. Workflow runs and job logs come from the **`actions`** toolset; `request_copilot_review` comes from the **`copilot`** toolset. Neither is on by default. | 2026-09-26 |
| <https://raw.githubusercontent.com/github/github-mcp-server/main/docs/remote-server.md> | The hosted server selects toolsets by URL path (`/mcp/x/<toolset>`) or by the `X-MCP-Toolsets` header, comma-separated. | 2026-09-26 |

## Archify

| Source | Establishes | Checked |
|---|---|---|
| <https://github.com/tt-a1i/archify> | The diagram skill used for the repository architecture diagrams. MIT licensed, v3.0.1 at time of use. | 2026-09-29 |
| <https://skills.sh/tt-a1i/archify> | The install path's security assessment page. It did not expose the individual findings; the package was audited by direct inspection instead. | 2026-09-29 |
| <https://tt-a1i.github.io/archify/skill-updates/archify/stable.json> | The single outbound endpoint the tool contacts, hardcoded with a guard that rejects any other URL. Disable with `ARCHIFY_UPDATE_CHECK_DISABLED=1`. | 2026-09-29 |

## Course material referenced in the proposal

| Source | Role |
|---|---|
| <https://learning.oreilly.com/course/aws-certified-ai/9780135420782/> | Recommended preparation — *AWS Certified AI Practitioner (AIF-C01)* by Chad Smith |
| <https://learning.oreilly.com/search/?q=Bruce%20Hopkins%20AI&type=live-course&rows=100&publishers=Pearson> | Recommended follow-up — *Create AI Agents with Model Context Protocol (MCP)* by Bruce Hopkins |

---

## Not verified — check before using on a slide

These come from the course refactor notes and were **not** confirmed while
building this material. Both would appear on slides, so both need checking.

| Claim | Where it came from | What to do |
|---|---|---|
| The MCP specification dated 2026-07-28 deprecates the legacy HTTP+SSE transport | Course refactor notes | Confirm against the published specification before stating it. The transport slides were cut on the strength of this. |
| The MCP context-bloat figure traces to a single user measurement in `claude-code` issue #11364, November 2025 | Course refactor notes | Confirm the issue exists and says what is claimed. The notes already say to present this as a shape rather than a benchmark — keep it that way. |

## Facts that have already changed once

Evidence that this file needs re-checking rather than trusting:

- Copilot code review **used to** have a fixed language list. It no longer does.
- Copilot billing moved from "one premium request" to AI credits with two effort levels.
- arm64 runners were public-repository only until January 2026.
- `configure-aws-credentials` is on v6; v4 is two majors behind.
- GitHub's OIDC subject claim now embeds immutable numeric owner and repository
  ids, so a trust policy matching the plain `owner/repo` form fails. Discovered
  by reading failed `AssumeRoleWithWebIdentity` events in CloudTrail.
