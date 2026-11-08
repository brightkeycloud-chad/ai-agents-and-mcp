# Development half — runbook

**Budget:** about 22 minutes of demonstration inside a 45-minute block.

Two reviewers look at the same pull request. One you build and own, one you
switch on. The point is not that either is better. It is that they see
different things, and knowing which is which tells you what to use each for.

## Before the session

- [ ] The environment is up, following the [environment runbook](../00-environment/RUNBOOK.md)
- [ ] A GitHub account with the repositories accessible, and a browser signed in to it
- [ ] `gh auth status` shows you signed in, because step 1 takes its token from `gh`
- [ ] A Copilot plan that includes code review (Pro, Pro+, Business, Enterprise or Max)
- [ ] `status-board-app` cloned and open in VS Code
- [ ] On `main`, with no agent file in `.claude/agents/` — you build that live
- [ ] the open pull request on `feat/post-incidents` open, CI green, **no review yet**
- [ ] A browser tab already signed in to GitHub

None of the steps below use the stack directly: the review works from the
repository and the pull request. It still has to be up before this half starts,
because the course runs on one environment throughout.

**Do not load the live board during this half.** If the DevOps breaking change
has already been merged, the board returns 504.

## Running it

### 1. Connect the GitHub MCP server — 3 min

From the terminal, not by editing a file. Run this before starting `claude`, and
**in `status-board-app`**. These entries belong to the directory you run them
from, so running `remove` anywhere else removes a different connection.

```bash
cd ~/Work/github/status-board-app
mkdir -p .claude/agents   # must exist before claude starts; see step 3
claude mcp remove github
export GITHUB_TOKEN=$(gh auth token)
claude mcp add --transport http github https://api.githubcopilot.com/mcp \
  --header "X-MCP-Toolsets: context,repos,issues,pull_requests,users,actions,copilot" \
  --header "Authorization: Bearer $GITHUB_TOKEN"
claude mcp list
```

Expect `github ... ✔ Connected`. If no entry exists yet, `remove` reports an error
that you can ignore. If `claude` is already running in this directory, restart it
to pick up the new entry.

**A token is required.** Without the `Authorization` header there is no browser
sign-in to fall back on: the connection fails with `Incompatible auth server:
does not support dynamic client registration`. Observed with Claude Code 2.1.319
on 2026-11-08.

**What to say about the token.** It comes from `gh` and is never typed on screen,
but `claude mcp add` saves it in plain text in `~/.claude.json`. Say so if anyone
asks. `add` redacts it in its own output.

**Do not run `claude mcp get github` on screen. It prints the token in full.**

**The part worth saying out loud.** The bare `/mcp` endpoint serves a *default*
toolset — `context, repos, issues, pull_requests, users` — and nothing else.
Two of the toolsets in the command above are off by default and both are needed
here: `actions` reads workflow runs and job logs, and `copilot` is what
requests a Copilot review on a pull request.

The server also ships `code_security`, `dependabot`, `discussions`, `gists`,
`notifications`, `projects`, `stargazers` and more. None are enabled, because
every tool you turn on spends context before you type a word. That is slide 22
arriving early, demonstrated rather than asserted.

### 2. Show `AGENTS.md` — 2 min

Open [`AGENTS.md`](https://github.com/brightkeycloud-chad/status-board-app/blob/main/AGENTS.md)
in the application repository. Five house rules, written once, read by every
agent that works here. Scroll to the Conventions section — rules 1 and 2 are
the ones the pull request breaks.

The infrastructure repository has its own, with different rules for Terraform.
Same idea, different domain: the standard lives beside the code it governs.

Say plainly that **Copilot reads this file too**. The comparison coming up is
not about one reviewer knowing the rules and the other not.

### 3. Build the review agent — 5 min

Ask Claude Code to generate it. Do not hand-write it on stage.

> Create a subagent called code-reviewer that reviews changes in this
> repository. Give it read-only access: Read, Grep and Glob only. It should
> read AGENTS.md first, follow what a change touches out into the rest of the
> repository, and separate findings it got from the diff from findings that
> needed other files.

Then show the generated file, and specifically the `tools:` line. Three tools.
It can read the code; it cannot change it. That is the whole of slide 13.

Commit it. A reviewer the team shares is a file in the repository, not a
setting in somebody's editor.

#### Loading the new agent

There is no reload prompt, and `/agents` does not reload anything. Claude Code
watches `.claude/agents/` and picks up a new file within a few seconds, but only
if that directory **existed when the session started**. That is why step 1
creates it.

Confirm it loaded before moving on:

> Which subagents can you delegate to? Is code-reviewer one of them? Answer from
> your available subagents, not by reading files.

**If it is not listed, restart.** This keeps the conversation:

```bash
/exit
claude --continue
```

Then ask the same question again. The behaviour above comes from the Claude Code
documentation. Starting from an empty `.claude/agents/` has not yet been rehearsed.

**If the generation goes sideways:** `code-reviewer.md` in this directory is a
known-good copy. Copy it to `.claude/agents/` and carry on.

### 4. Start both reviews — 2 min

**Run them at the same time.** Neither is instant, and waiting for one before
starting the other spends minutes you do not have.

Ask Claude Code to review the open pull request with the subagent. It reaches the pull request
through the GitHub MCP. The subagent itself has only Read, Grep and Glob, so it
cannot fetch the diff — the main thread hands it over. Say that out loud; it is
the scoping made visible.

While it runs, switch to the browser and request a Copilot review on the same
pull request from the reviewers list.

Now both are working. Use the wait rather than apologising for it: this is two
reviewers looking at one change, which is the whole point of the block.

### 5. Read what came back — 8 min

The subagent takes **three to four minutes** and reports **a dozen or more
findings**. That is measured, not estimated. Do not try to read them all on
screen — scroll to its last section, headed "Which findings came from where."

**Copilot returns about ten findings**, graded by severity and attached to
lines.

#### Read this before the session

**Copilot code review reads files the pull request does not touch.** Measured
on 2026-11-07: it named `VALID_STATUSES` by identifier and listed the three
statuses `board.html` renders, neither of which appears in the diff or in
`AGENTS.md`. In September the documentation gave no indication it could do
this. It can now.

So **do not claim Copilot only sees the diff.** It found the blank-tile bug and
the missing test, both of which earlier drafts of this runbook promised it
would miss. Someone in the room will have read the same documentation you did,
and the claim is checkable in front of them.

#### What each one actually found

Both found, and Copilot graded them well: PartiQL built by string formatting,
no transactional guarantee across the three writes, no service-existence check,
validation not going through the shared validators, DynamoDB reached outside
the storage layer, an unpaginated count, no response model, no tests, and the
`outage` status rendering without a badge.

The subagent additionally found, and Copilot did not:

- **PartiQL is authorised by its own IAM actions** — `dynamodb:PartiQLInsert`,
  `PartiQLUpdate`, `PartiQLSelect` — and the task role grants only
  `PutItem`/`UpdateItem`/`Query`. **This change would fail with `AccessDenied`
  in AWS while every test passed.** The agent reasoned that about
  `status-board-infra`, a repository it could not read, and said so rather than
  asserting it.
- **The new client ignores `DYNAMODB_ENDPOINT_URL`**, so under `docker compose`
  this one route talks to real AWS while every other route talks to the local
  database.
- **`tests/test_validators.py:54` already asserts `outage` is invalid.** The
  repository would hold a test and a route that contradict each other, and CI
  stays green because the route never calls the validator.
- **`store.py`'s own docstring becomes false** — it says "nothing in this
  codebase uses PartiQL" — in a file the diff never touches.
- **The committed architecture diagram goes stale**, and because its candidate
  pins an old commit the renderer keeps validating happily.

### 6. Compare — 2 min, then discussion

Put them side by side. The honest reading:

> Copilot reviewed the change. It did that well, and it reached further than
> its own documentation said it would. What it did not do is work out that this
> code cannot run in our account at all, because PartiQL needs IAM permissions
> our task role does not grant — and it could not, because that lives in
> another repository. My agent reasoned its way there and then told me it was
> not certain. That is the difference worth paying for: not more findings, but
> knowing where the edge of its knowledge is.

Two things worth saying plainly:

**The product changed while this course was being built.** In September,
Copilot code review could not read past the diff. By November it could. The
comparison in an earlier draft of this material was true when written and false
three weeks later. That is slide 33 arriving early and unprompted — the
products will change, and the principles are what you keep.

**Neither reviewer is the answer.** One runs on your machine, scoped by you,
and can be pointed at anything you can read. The other runs on GitHub, needs no
setup from anyone, and arrives in the place the team already works. Most teams
end up wanting both.

Then the closing question: **an agent you own, or a service you switch on?**

## Resetting between runs

Copilot review comments accumulate and cannot be deleted from a pull request,
so each rehearsal gets a fresh one. GitHub does not allow deleting a pull
request at all — only closing it — so the old one stays in the list, closed.

```bash
cd status-board-app

# 1. Retire the reviewed pull request and recreate the branch untouched.
PR=$(gh pr list --head feat/post-incidents --json number --jq '.[0].number')
gh pr close "$PR"
git push origin --delete feat/post-incidents
git push origin d85e10f:refs/heads/feat/post-incidents

# 2. Open a clean one.
gh pr create --base main --head feat/post-incidents \
  --title "Allow posting incident updates" \
  --body-file ../ai-agents-and-mcp/demos/01-development/pr-body.md

# 3. Undo anything built live.
git checkout main
rm -rf .claude/agents
```

`d85e10f` is the commit carrying the planted change; it never moves. If you
committed the subagent during step 3, revert that commit too.

Check before the next run: the pull request shows **0 reviews, 0 comments**,
CI is green, and the branch contains no `.claude/`.

## Things that can go wrong

| Problem | What to do |
|---|---|
| Copilot review is slow | Request it at the start of step 5 and keep talking; it arrives within a minute or two |
| Claude says code-reviewer does not exist, or reviews the change itself | The session started before `.claude/agents/` existed. Run `/exit`, then `claude --continue` |
| Generation produces a different agent | Use the copy in this directory, and say you are using a prepared one |
| The subagent reports nothing from outside the diff | Check `tools:` includes Grep; without it the agent cannot search |
| The subagent asks for the diff and stops | It has no shell and no GitHub MCP. Paste the diff, or have the main thread fetch it first |
| The review runs long | Expected. Start it before the Copilot request so both run together |
| Someone asks whether Copilot could be given the same reach | Good question, and the honest answer is that custom instructions tell it the rules but do not let it open an untouched file |
| `claude mcp list` shows `Incompatible auth server: does not support dynamic client registration` | The entry has no `Authorization` header. In `status-board-app`, run the step 1 commands again |
| `claude mcp list` shows another connection failure | Check `gh auth status`, because an empty or expired token cannot connect. Sign in with `gh auth login`, then run the step 1 commands again |
| The Copilot review option is missing from the reviewers list | The `copilot` toolset is not what puts it there — that is the GitHub UI, and it needs a Copilot plan on the account that owns the repository |
