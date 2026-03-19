---
name: watch-pr
description: Watch a PR and resolve every unresolved comment. Use when monitoring pull requests, babysitting PRs, waiting for reviews, or tracking CI status on an open PR. One job — zero unresolved comments.
argument-hint: "[pr-number]"
disable-model-invocation: true
---

If a PR number is provided as `$ARGUMENTS`, use that. Otherwise, detect the PR for the current branch by running `gh pr view --json number -q .number`. If no PR is found, tell the user and stop.

Derive the repo owner/name from the current git remote (`gh repo view --json owner,name`).

Launch two background agents that run concurrently. Both agents must keep running until the PR is merged or closed — never stop early.

**Critical: both agents must check current state immediately on launch, before entering their polling loops.** Pre-existing failures, unresolved comments, or other issues from before the watcher started are just as important as new ones.

---

## Agent 1: Comment Resolver

**Your one job: zero unresolved comments on this PR.**

Every poll cycle, fetch ALL review threads and find every unresolved one. It doesn't matter if a comment is old or new — if it's unresolved, it's your problem.

### How to find unresolved comments

**On launch, immediately run your first check.** Then continue polling every **30 seconds**. On each cycle, use the GraphQL API to get all review threads with their resolution status:

```bash
gh api graphql -f query='
{
  repository(owner: "{owner}", name: "{repo}") {
    pullRequest(number: {pr}) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          comments(first: 10) {
            nodes {
              id
              author { login }
              body
              path
              line
              createdAt
            }
          }
        }
      }
    }
  }
}'
```

Filter to threads where `isResolved` is `false`. These are your targets.

Also check PR state each cycle: `gh pr view <pr> --json state -q .state`. Stop only when `MERGED` or `CLOSED`.

### Handling each unresolved thread

For each unresolved thread, read the comment(s) and decide:

1. **You can fix it yourself** — the comment asks for a code change, naming fix, typo, style issue, or something you can confidently address. Do it: make the code change, reply to the comment explaining what you did, and resolve the thread. Push the fix. Tell the user what you did.

2. **You can reply and resolve** — the comment is a question you can answer, a bot comment, an FYI, or something that doesn't need a code change. Reply with a clear answer and resolve the thread. Tell the user what you did.

3. **You need the user** — the comment raises a design question, asks for a judgment call, or is ambiguous enough that you shouldn't act alone. Surface it to the user immediately:
   - **Who** commented
   - **Where** — file:line if inline, "PR-level" otherwise
   - **What** they said — quote the full text
   - **Why you need them** — what decision is needed
   - Wait for the user's instruction, then act on it, reply, and resolve.

Bias toward action. If you can handle it, handle it. Only escalate to the user when you genuinely can't decide the right course.

### Resolving threads

After replying to a comment, resolve the thread:

```bash
gh api graphql -f query='
mutation {
  resolveReviewThread(input: {threadId: "{thread_id}"}) {
    thread { isResolved }
  }
}'
```

### Tracking what you've handled

Keep a set of thread IDs you've already resolved or escalated to the user. Don't re-surface threads you're waiting on user input for — but do re-check them if the user hasn't responded after 2 minutes, with a gentle reminder.

### The goal

Every cycle should end with you either having resolved all threads, or actively waiting on the user for the ones you couldn't handle yourself. If the unresolved count is zero, say nothing — just keep watching. If new unresolved threads appear, handle them immediately.

---

## Agent 2: CI Monitor

**On launch, immediately check current CI status** — don't wait for the first poll interval. If checks have already failed before you started watching, handle them right away using the failure logic below. Then continue polling every **60 seconds** using `gh pr checks <pr>`.

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
