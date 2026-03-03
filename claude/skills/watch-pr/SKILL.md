---
name: watch-pr
description: Watch a PR for new comments and CI failures
argument-hint: "[pr-number]"
disable-model-invocation: true
---

If a PR number is provided as `$ARGUMENTS`, use that. Otherwise, detect the PR for the current branch by running `gh pr view --json number -q .number`. If no PR is found, tell the user.

Launch two background agents:

1. **PR Comment Watcher**: Check every 60 seconds for new review comments and PR comments using `gh pr view <pr> --json comments` and `gh api repos/{owner}/{repo}/pulls/<pr>/comments`. Track seen comments and only report new ones. Surface comment author, content, and file/line location to the user for decisions. Do NOT address comments autonomously. once addressed, always comment and resolve the bot PRs. For the user initiated PRs, give me a response so I can type there manually.

2. **CI Monitor**: Check every 90 seconds for CI check status using `gh pr checks <pr>` and `gh run list`. If a check fails, inspect logs with `gh run view <run-id> --log-failed`. If the failure looks flaky (transient error, timeout, unrelated to PR changes), rerun with `gh run rerun <run-id> --failed`. If it looks like a legitimate failure, report details to the user. Stop when all checks are green.

Both agents should run in the background concurrently. Derive the repo owner/name from the current git remote.
