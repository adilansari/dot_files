# Claude Code Skills

## Personal Preferences

- I prefer concise, direct responses
- Explain me first, then ask if I need to see the code or have any followups

## Coding Style

- Follow existing project conventions when working in established codebases
- Prefer simple solutions over clever ones

## Workflow

- Before making changes, understand the existing code structure
- Make incremental changes that are easy to review
- When debugging, explain the root cause, not just the fix
- Always use signed commits (`git commit -S`)
- Prefer launching subagents for parallelizable work — e.g., fixing multiple bugs, replying to several PR comments, researching across files. If tasks are independent, run them concurrently via the Agent tool rather than doing them sequentially.

## GitHub

- When replying to PR review comments, always reply **in the thread** (on the specific comment), never as a top-level PR comment.
  - PR review comments (inline code comments from reviewers/bots) live under `pulls/{pr}/comments`. List them with: `gh api repos/{owner}/{repo}/pulls/{pr}/comments`
  - To reply in-thread: `gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies -f body="..."`
  - **Never** use `gh pr comment` or `gh api repos/{owner}/{repo}/issues/{pr}/comments` to respond to review feedback — those create top-level comments that are disconnected from the review thread.
  - Issue comments (`issues/{pr}/comments`) and PR review comments (`pulls/{pr}/comments`) are different APIs. Review comments have `diff_hunk`, `path`, and `line` fields. Always check which type you're dealing with before replying.

## Writing & Communication

- Always use the `/adil-voice` skill when writing content that will be read by others — emails, Slack messages, PR descriptions, docs, design docs, blog posts, and general explanations. If it represents my voice, run the skill.

## Tools & Environment

- Primary shell: zsh with oh-my-zsh
- Editor: neovim (nvchad)
- Terminal multiplexer: tmux
- OS: macOS
