#!/bin/bash

cd $HOME

# Check to make sure dotfiles is located at $HOME/dot_files
dot_files_dir="$HOME/dot_files"

if [[ ! -d $dot_files_dir ]]; then
  echo "Could not find dotfiles directory. Make sure you place it under $HOME"
  exit 1
fi

# following are file or directory names under which files should be looked into
filenames=(
	'zsh'
	'vim'
	'tmux'
	'git'
	'.ctags'
	'.bash_profile'
) 

# Create symlinks for dot_files
# ln -sf source_file target_file
create_symlink() {
	ln -sf $1 .
	echo "creating symlink for $1"
}

# iterate over given file/directory names
for name in ${filenames[@]}; do
	path=$dot_files_dir/$name
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
