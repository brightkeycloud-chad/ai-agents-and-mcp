# Development half — runbook

**Budget:** about 22 minutes of demonstration inside a 45-minute block.

Two reviewers look at the same pull request. One you build and own, one you
switch on. The point is not that either is better. It is that they see
different things, and knowing which is which tells you what to use each for.

## Before the session

- [ ] GitHub MCP server connected, with the `copilot` and `repos` toolsets
- [ ] A Copilot plan that includes code review (Pro, Pro+, Business, Enterprise or Max)
- [ ] `status-board-app` cloned and open in VS Code
- [ ] On `main`, with **no** `.claude/agents/` directory — you build that live
- [ ] [PR #1](https://github.com/brightkeycloud-chad/status-board-app/pull/1) open, CI green, **no review yet**
- [ ] A browser tab already signed in to GitHub

No AWS resources are needed. The stack can stay destroyed.

## Running it

### 1. Connect the GitHub MCP server — 3 min

From the terminal, not by editing a file. Show that it is one command and that
credentials are handled by the authorisation flow.

Point out that the server ships more toolsets than you enabled. Every tool you
turn on costs context before you type a word, so you enable what the work needs
and leave the rest off. That is slide 22 arriving early, which is fine.

### 2. Show `AGENTS.md` — 2 min

Open it in the repo. Five house rules, written once, read by every agent.

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

**If the generation goes sideways:** `code-reviewer.md` in this directory is a
known-good copy. Copy it to `.claude/agents/` and carry on.

### 4. Review the pull request with it — 6 min

Ask Claude Code to review PR #1 using the subagent. It reaches the pull request
through the GitHub MCP.

Expect it to find, from the diff: PartiQL built by string formatting, no error
handling on the write, a hand-rolled regex where `validators.py` already has
one, `boto3` imported into a route module, and a raw dict returned instead of a
model.

And expect it to find, by reading files the pull request never touches:

- `"outage"` is accepted but `app/templates/board.html` has no branch for it,
  so the tile renders blank
- the write and the read-back duplicate `store.put_incident` and
  `store.list_incidents`
- no test was added to `tests/test_api.py`

### 5. Ask Copilot to review the same pull request — 4 min

In the browser, request a review from the reviewers list. Let it run while you
talk.

It should do well on the first group. Its comments arrive graded by severity,
attached to lines, in the place the team already works.

### 6. Compare — 2 min, then discussion

Put the two side by side. The honest reading:

> Copilot read the same `AGENTS.md` my agent did. It caught the injection and
> the convention break. What it could not do is open `board.html`, a file this
> pull request never touches, and notice the new status has nowhere to render.
> That is not a smarter model. That is access.

Then the closing question: **an agent you own, or a service you switch on?**

The answer is usually both, for different jobs. One runs on your machine,
scoped by you, reading whatever you allow. The other runs on GitHub, sees the
diff plus your instruction files, and needs no setup from anyone.

## Resetting between runs

```bash
cd status-board-app
git checkout main
rm -rf .claude/agents          # if you committed it live, revert that commit too
```

On the pull request, dismiss or delete the Copilot review so the next run starts
clean. The branch and the pull request stay; nothing is merged.

## Things that can go wrong

| Problem | What to do |
|---|---|
| Copilot review is slow | Request it at the start of step 5 and keep talking; it arrives within a minute or two |
| Generation produces a different agent | Use the copy in this directory, and say you are using a prepared one |
| The subagent reports nothing from outside the diff | Check `tools:` includes Grep; without it the agent cannot search |
| Someone asks whether Copilot could be given the same reach | Good question, and the honest answer is that custom instructions tell it the rules but do not let it open an untouched file |
