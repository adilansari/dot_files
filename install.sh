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
  "tmux/scripts:.tmux-scripts"
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

# Create symlinks for dot_files
# ln -sf source_file target_file
create_symlink() {
	echo "creating symlink for $1 to $2"
	ln -sf $1 $2
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

# Per-skill symlinks: ~/.claude/skills/ is kept as a real directory so
# third-party skill installers (e.g. antithesis-skills) can drop their own
# symlinks alongside ours without colliding with a whole-directory symlink.
mkdir -p "$HOME/.claude/skills"
for skill_dir in "$DOT_FILES_DIR"/claude/skills/*/; do
  skill_name=$(basename "$skill_dir")
  create_symlink "${skill_dir%/}" "$HOME/.claude/skills/$skill_name"
done

# Prune skill symlinks whose repo source was deleted. Scope to this repo's
# skills dir so third-party skill symlinks (e.g. antithesis-skills) are untouched.
#
# TODO: once both Macs are migrated, also purge residual watch-pr mentions from
# machine-local ~/.claude artifacts (backups, file-history, history.jsonl, transcripts).
for link in "$HOME"/.claude/skills/*; do
  [[ -L "$link" ]] || continue
  dest=$(readlink "$link")
  case "$dest" in
    "$DOT_FILES_DIR"/claude/skills/*)
      if [[ ! -e "$dest" ]]; then
        echo "removing stale skill symlink $link -> $dest"
        rm "$link"
      fi
      ;;
  esac
done

exit 0
