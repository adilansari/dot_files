#!/bin/bash

DOT_FILES_DIR="$(pwd)/dot_files"

if [[ ! -d $DOT_FILES_DIR ]]; then
  echo "Could not find dotfiles directory. Make sure you are in the directory where repo is cloned."
  exit 1
fi

# following are file or directory names to create symlinks
# by default, all symlinks are created to $HOME
# but you can specify a different target using colon : delimiter
linktargets=(
  "zsh/.zsh"
  "zsh/.zshrc"
  "vim/.vimrc"
  "tmux/.tmux.conf"
  "tmux/.tmuxinator"
  "tmux/scripts:$HOME/.tmux-scripts"
  "git/.git-completion.bash"
  "git/.gitconfig"
  "git/.gitignore"
  ".bash_profile"
  "config/gh-dash:$HOME/.config"
  "config/htop:$HOME/.config"
  "config/nvim/mappings.lua:$HOME/.config/nvim/lua"
  "config/nvim/options.lua:$HOME/.config/nvim/lua"
  "zsh/.zsh/.p10k.zsh:$HOME/.p10k.zsh"
  "claude/CLAUDE.md:$HOME/.claude"
)

create_symlink() {
	echo "creating symlink for $1 to $2"
	ln -sfh $1 $2
}

# iterate over given file/directory names
for item in ${linktargets[@]}; do
  source=${item%%:*}
  target=${item#*:}
  if [[ -z "$target" || "$target" = "$source" ]]; then
    target=$HOME
  fi
  create_symlink $DOT_FILES_DIR/$source $target
done

# ~/.claude/skills/ and hooks/ stay real dirs, not whole-directory symlinks: a whole-dir
# symlink would collide with third-party installers (e.g. antithesis-skills) that drop their
# own entries in. The case match keeps pruning to this repo's paths so those entries survive.
#
# TODO: once both Macs are migrated, also purge residual watch-pr mentions from
# machine-local ~/.claude artifacts (backups, file-history, history.jsonl, transcripts).
link_claude_dir() {
  local name="$1" glob="$2" dest="$HOME/.claude/$1"
  mkdir -p "$dest"
  for src in "$DOT_FILES_DIR"/claude/"$name"/$glob; do
    [[ -e "$src" ]] || continue
    create_symlink "${src%/}" "$dest/$(basename "$src")"
  done
  for link in "$dest"/*; do
    [[ -L "$link" ]] || continue
    local target
    target=$(readlink "$link")
    case "$target" in
      "$DOT_FILES_DIR"/claude/"$name"/*)
        if [[ ! -e "$target" ]]; then
          echo "removing stale symlink $link -> $target"
          rm "$link"
        fi
        ;;
    esac
  done
}

link_claude_dir skills '*/'
link_claude_dir hooks '*.sh'

# Patch the comment-audit hook into machine-local settings.json (gitignored, so not in the
# repo). Seed {} when absent so a fresh machine, where the file doesn't exist yet, still gets
# patched instead of silently skipped.
settings="$HOME/.claude/settings.json"
if command -v jq >/dev/null 2>&1; then
  [[ -f "$settings" ]] || echo '{}' > "$settings"
  if ! grep -q 'comment-audit.sh' "$settings"; then
    tmp=$(mktemp)
    if jq '.hooks.PostToolUse += [{"matcher":"Edit|Write|MultiEdit","hooks":[{"type":"command","command":"sh \"$HOME/.claude/hooks/comment-audit.sh\""}]}]' "$settings" >"$tmp"; then
      mv "$tmp" "$settings"
      echo "registered comment-audit hook in $settings"
    else
      rm -f "$tmp"
      echo "WARN: could not patch $settings (invalid JSON?); left unchanged"
    fi
  fi
fi

exit 0
