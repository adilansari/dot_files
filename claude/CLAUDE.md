# Claude Code Skills

## Personal Preferences

- I prefer concise, direct responses
- Explain me first, then ask if I need to see the code or have any followups
- Be direct. Lead with the answer or action, not the reasoning.
- When I push back or ask for changes, do it — don't explain why the original was fine.
- I prefer to stay in control of the direction. Propose, don't decide.

## Planning & Architecture

When creating plans (plan mode, /architect, or any design/implementation planning):

### 1. Always Ground in Project Context
- Read the project's CLAUDE.md (and any referenced sub-docs like test/CLAUDE.md, workers/CLAUDE.md) BEFORE proposing anything
- Reference specific conventions, patterns, and utilities found there — don't reinvent what already exists
- If there's no CLAUDE.md, say so and ask what conventions matter

### 2. No Unnecessary Assumptions
- Always pause and ask when the intent is ambiguous rather than guessing
- If a decision has multiple valid approaches, present them with trade-offs and let me choose
- Don't assume scope — if the request is vague, clarify before planning
- Don't assume tech choices, naming conventions, or architectural patterns without checking what the project already uses

### 3. Show Me the Code
- Every plan must include concrete code samples for key changes — not just descriptions of what will change
- Show before/after snippets for modifications to existing code
- Show full function/struct signatures for new code
- For complex flows, include a short code sketch showing how the pieces connect
- If a plan only has prose and no code, it's incomplete

### 4. Present Complete Plans, Then Iterate
- Do the research independently, then present a complete plan with code samples
- After presenting, explicitly ask: "What would you change about this approach?"
- Revise based on feedback — don't just acknowledge it, show the updated plan
- One round-trip of feedback is normal; don't rush to implementation

### 5. PR Lifecycle — Close the Loop
- If the work produces code changes that will be pushed and a PR created, the plan's final step must include: create PR → run `/watch-pr` to subscribe to CI and review activity
- This applies to any work-related code (features, fixes, refactors). Skip for non-code tasks (docs-only, local config, research)
- Don't ask whether to watch — just include it as a standard closing step in the plan

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
