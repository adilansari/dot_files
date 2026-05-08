---
name: review-comments
description: Process CLAUDE_FIX / CLAUDE_EXPLAIN / CLAUDE_REVIEW markers the user has left as inline comments in source code. Use whenever the user says they've "left comments", "left review comments", "added markers", "left feedback in the code", or asks to "process / handle / check my comments / markers". Also triggers on phrases like "I'm done reviewing" in the context of a Claude-authored changelist. Greps the working tree for CLAUDE_* markers, handles each per its prefix, and leaves the result as an uncommitted changelist for the user to re-review. Does not commit or create PRs.
---

# Review Comments

The user reviews Claude-authored changes in IntelliJ and leaves inline markers prefixed with `CLAUDE_FIX:`, `CLAUDE_EXPLAIN:`, or `CLAUDE_REVIEW:` for things they want addressed. They commit anything they're already happy with, leaving the markers in a fresh changelist. This skill turns those markers into a reviewable response.

## The loop this fits into

1. Claude writes code → user reviews → leaves CLAUDE_* markers
2. User commits anything they're already happy with
3. User triggers this skill
4. Skill processes markers → leaves new uncommitted changelist
5. User re-reviews → back to step 2 until no markers remain

Commit, push, and PR creation are the user's job. Stay out of them.

## Discovery

```bash
git grep -nE "CLAUDE_(FIX|EXPLAIN|REVIEW):"
```

If nothing matches, tell the user and stop — silence means there's nothing for you to do, don't go fishing for issues yourself.

For each match, read the surrounding code (the comment block, the line(s) it refers to, related code nearby). A marker on line 42 might be about the function above, the line below, or the whole block — read enough to be sure.

## Per-prefix behavior

### CLAUDE_FIX
Implement exactly what the comment describes. Don't expand scope, don't refactor adjacent code, don't add tests unless the comment asks for them. Then remove the marker line(s) entirely.

### CLAUDE_EXPLAIN
Answer in chat. Do not change the code. Remove the marker after answering — if the user wants to ask more, they'll add another.

### CLAUDE_REVIEW
The user is flagging a concern with multiple plausible resolutions. In chat, present:
- One sentence on what you think the concern is (so they can correct you)
- 2-3 concrete options with trade-offs
- A recommendation

Do not touch the code yet. Wait for the user's pick, then apply and remove the marker. If you genuinely can't think of 2+ options, ask a clarifying question instead of inventing weak alternatives.

## Marker removal

Remove the whole comment line(s), not just the prefix word. If the marker spans multiple lines, remove all of them. Don't leave dangling `//` or `#` shells.

## End-of-run summary

Print a short table so the user can sanity-check before re-reviewing in their editor:

```
file:line   prefix          action
foo.go:42   CLAUDE_FIX      renamed `x` to `userID`
bar.go:17   CLAUDE_EXPLAIN  answered in chat (see above)
baz.go:88   CLAUDE_REVIEW   awaiting your pick (3 options above)
```

If any CLAUDE_REVIEW markers are still pending, call it out — the changelist isn't done until those are resolved.

## Edge cases

- **Marker inside a string literal**: `git grep` may match these. Read the file and skip if it's not a real comment.
- **Marker that no longer makes sense** (surrounding code drifted): ask rather than guess.
- **Multiple markers on the same chunk**: handle top to bottom in file order.
- **Marker outside the working tree** (already committed): out of scope. Only process what `git grep` finds in the working tree.

## What this skill does NOT do

- Commit, push, or create/update PRs
- Touch committed code
- Add markers of its own
- Refactor or "clean up" code the user didn't ask about
