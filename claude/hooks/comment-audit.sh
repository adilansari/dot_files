#!/usr/bin/env sh
# PostToolUse gate for the comment rule in ~/.claude/CLAUDE.md (§Comments). The pass keeps getting
# skipped from memory, so this makes it mechanical: after any Edit/Write/MultiEdit that adds comment
# lines to a source file, list exactly those lines and block (exit 2) with the deletion test. It does
# NOT judge quality — it forces the test to be run on each added comment before moving on, so a
# restatement can't slip through unseen.
command -v jq >/dev/null 2>&1 || exit 0

# stdin is a pipe, readable once — slurp it, then query the copy twice.
INPUT=$(cat)

FILE=$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
case "$FILE" in
  *.go|*.py|*.ts|*.tsx|*.js|*.jsx|*.rs|*.sh|*.java|*.rb|*.c|*.h|*.cpp|*.cc|*.kt|*.swift| \
  *.yml|*.yaml|*.j2|*.jinja|*.jinja2| \
  *.service|*.timer|*.socket|*.mount|*.path|*.target|*.network|*.link|*.netdev|*.rules| \
  *.just|*Justfile|*justfile|*Makefile|*makefile| \
  *Dockerfile|*dockerfile|*Containerfile|*.tf|*.tfvars|*.hcl|*.nix| \
  *.toml|*.ini|*.cfg|*.conf|*Caddyfile|*Vagrantfile) : ;;
  *) exit 0 ;;
esac

# Text this edit introduced: Edit=new_string, Write=content, MultiEdit=all edits' new_string.
ADDED=$(printf '%s' "$INPUT" | jq -r '.tool_input.new_string // .tool_input.content // ([.tool_input.edits[]?.new_string] | join("\n")) // empty' 2>/dev/null)
[ -n "$ADDED" ] || exit 0

# Human comment lines only — drop shebangs, tool directives, modelines, and script-runner headers.
COMMENTS=$(printf '%s\n' "$ADDED" \
  | grep -E '^[[:space:]]*(//|#)' \
  | grep -vE '^[[:space:]]*(//go:|#!|# *shellcheck|# *-\*-|# *vim:|#name=|#description=|#arrayStarted)' \
  || true)
[ -n "$COMMENTS" ] || exit 0

{
  echo "COMMENT-RULE GATE — this edit added these comment lines to $FILE:"
  printf '%s\n' "$COMMENTS" | sed 's/^/    /'
  echo
  echo "Run the DELETION TEST on EACH now, before continuing (~/.claude/CLAUDE.md §Comments):"
  echo "delete the comment, then name the exact wrong assumption a reader makes without it."
  echo "No concrete misread → DELETE it. Keep only a non-obvious why: a hidden invariant, a"
  echo "surprising workaround, or an external contract. Godoc that restates a private helper or"
  echo "test is the #1 miss — cut it."
  echo "Reply per line: KEEP <the exact misread it prevents> or DELETE, then make the edits."
} >&2
exit 2
