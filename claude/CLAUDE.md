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
- New-file copyright headers: never default to a hardcoded year. Match a recently-added file in the same project, or use the current year if none — never a stale one from training data.

## Comments

**Do this every time: before you present or commit code you wrote, make a dedicated comment pass.** Re-read every comment you added and delete any that fail the bar below. This is a required final step on a coding task — the same standing as signed commits, not "if you remember." Your default is to over-comment; this pass is what counters it.

A comment earns its place only when the *why* is non-obvious to someone reading the code cold:
- a hidden invariant or business rule the code enforces
- a surprising behavior or workaround for a specific bug
- a constraint imposed from outside (ordering, atomicity, external API quirk)

**A kept comment must be self-contained.** Assume the reader has only this file open and has never read the design doc. It may not name a tier, phase, layer, signal, or any term the code in this file doesn't define — no "(Tier 1)", no "Tier-3 switch", no vocabulary lifted from an RFC. If the comment can't be understood without leaving the file, it's broken: state the actual reason in plain words ("returns nil so the caller skips wiring and boot dodges chstore.New's log.Fatal"), or delete it.

Delete on sight:
- **Restatements** — paraphrases the line below it.
- **Godoc on small private helpers or tests** — the name and body already say it.
- **Type/package docs that restate the name** or inventory what's inside — the declarations say it.
- **Narration of library/driver behavior** — it's documented upstream, don't re-explain it.
- **Forward-references** to commits/PRs/"future work" — they rot on merge.
- **Provenance / design-doc essays** inline — link from a doc instead.
- **Anything over 1-2 lines** — if it needs more, fix the code or the name.

Default to no comment. If you reach for one, first ask whether a better name or smaller function removes the need.

**The test is deletion, not justification.** Delete the comment, then name the exact wrong assumption a reader makes without it. Can't name one, it stays deleted. "Explains the why", "documents intent", "notes the constraint" is how restatements survive. A true statement is never a reason to keep a comment, only a concrete misread prevented is. This applies to every comment in code you touch, not only ones you add.

Most common miss — godoc that restates a self-evident helper. The fix is to delete it; if an invariant matters, document it once on the struct field, not on every helper that touches it:
```go
// Bad — restates the body, plus a provenance essay:
// applyPaymentVerifiedAtPatch encodes the atomic mutual-exclusion semantics for
// payment_verified_at; stamping a non-zero verifiedAt also clears the required
// flag (see docs/...§Admin override). Clearing leaves the required flag alone.
func applyPaymentVerifiedAtPatch(meta *api.NamespaceMetadata, verifiedAt *timestamppb.Timestamp) { ... }

// Good — no godoc; the name and body carry it:
func applyPaymentVerifiedAtPatch(meta *api.NamespaceMetadata, verifiedAt *timestamppb.Timestamp) { ... }
```

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
