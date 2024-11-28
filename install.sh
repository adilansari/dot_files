#!/bin/bash

DOT_FILES_DIR="$(pwd)/dot_files"

if [[ ! -d $DOT_FILES_DIR ]]; then
  echo "Could not find dotfiles directory. Make sure you are in the directory where repo is cloned."
  exit 1
fi

# following are file or directory names under which files should be looked into
filenames=(
	'zsh'
	'vim'
	'tmux'
	'git'
	'.bash_profile'
	'config'
) 

# Create symlinks for dot_files
# ln -sf source_file target_file
create_symlink() {
	echo "creating symlink for $1 to $HOME"
	ln -sf $1 $HOME
}

# iterate over given file/directory names
for name in ${filenames[@]}; do
	path=$DOT_FILES_DIR/$name
	if [[ -d $path ]]; then
		for f in $path/.*; do
			create_symlink $f
		done
	elif [[ -f $path ]]; then
		create_symlink $path
	else
		echo "invalid filename"
	fi
done

exit 0
