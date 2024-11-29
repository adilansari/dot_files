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
  "git/.git-completion.bash"
  "git/.gitconfig"
  "git/.gitignore"
  ".bash_profile"
  "config/gh-dash:$HOME/.config"
  "config/htop:$HOME/.config"
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

exit 0
