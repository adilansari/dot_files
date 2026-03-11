---
name: watch-pr
description: Watch a PR for new comments and CI failures. Use when monitoring pull requests, babysitting PRs, waiting for reviews, or tracking CI status on an open PR.
argument-hint: "[pr-number]"
disable-model-invocation: true
---

If a PR number is provided as `$ARGUMENTS`, use that. Otherwise, detect the PR for the current branch by running `gh pr view --json number -q .number`. If no PR is found, tell the user and stop.

Derive the repo owner/name from the current git remote (`gh repo view --json owner,name`).

Launch two background agents that run concurrently. Both agents must keep running until the PR is merged or closed — never stop early.

---

## Agent 1: Comment Watcher

Poll every **30 seconds** for new comments. Use both of these on every poll cycle — each catches comments the other misses:
- `gh pr view <pr> --json comments,reviews` — PR-level comments and review summaries
- `gh api repos/{owner}/{repo}/pulls/<pr>/comments` — inline review comments on specific lines

### Tracking seen comments

On the first poll, snapshot all existing comment IDs as "already seen" — do not surface these. On every subsequent poll, compare against the seen set. Any comment with a new ID is new. Add it to the seen set immediately after surfacing it.

Every comment matters. Never skip, batch, or delay a comment. If you find new comments, surface them to the user **right away** before the next sleep cycle.

### Surfacing comments to the user

For each new comment, show:
- **Who** commented
- **Where** — file and line number if it's an inline comment, or "PR-level" otherwise
- **What** they said — quote the full comment text

Then suggest one of these actions:
1. **Reply & resolve** — draft a reply for the user to approve, then post it and resolve the thread (for bot comments or straightforward clarifications)
2. **Fix code** — describe what code change you'd make, but **wait for the user's approval** before touching anything
3. **Clarify** — draft a clarifying question to post as a reply

Wait for the user to tell you which action to take (or give their own instruction) before proceeding. Never fix code or reply autonomously.

### Stopping condition

Check `gh pr view <pr> --json state -q .state` each cycle. Stop only when state is `MERGED` or `CLOSED`.

---

## Agent 2: CI Monitor

Poll every **60 seconds** for CI check status using `gh pr checks <pr>`.

### On failure

When a check fails:
1. Inspect logs: `gh run view <run-id> --log-failed`
2. Determine if the failure is **flaky** (network timeout, transient infra error, unrelated to PR changes) or **legitimate** (test failure, lint error, build break related to PR changes)
3. If flaky — rerun with `gh run rerun <run-id> --failed` and tell the user you reran it
4. If legitimate — report the failure details to the user: which check, the relevant log lines, and your assessment of the root cause. Ask the user how they want to proceed before making any changes.

### On success

When all checks go green, report it to the user — but **keep polling**. New commits or force-pushes trigger new CI runs, so the monitor must keep watching.

### Stopping condition

Check `gh pr view <pr> --json state -q .state` each cycle. Stop only when state is `MERGED` or `CLOSED`.
