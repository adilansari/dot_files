#!/bin/bash
# Create symlinks for .dotfiles
# ln -sf source_file target_file

#ln -sf ~/.dotfiles/zsh/zshrc ~/.zshrc
#ln -sf ~/.dotfiles/zsh ~/zsh
#ln -sf ~/.dotfiles/vim/.vimrc ~/.vimrc
#ln -sf ~/.dotfiles/tmux/.tmux.conf ~/.tmux.conf
#ln -sf ~/.dotfiles/tmuxinator/.tmuxinator/* ~/.tmuxinator
#ln -sf ~/.dotfiles/git/.* ~
#ln -sf ~/.dotfiles/bash/.* ~


# Copy the files listed in the array thats it
filenames=(
	'.zshrc'
	'.bash_profile'
	'.zsh'
	'.vimrc'
	'.tmux.conf'
	'.tmuxinator'
	'.gitconfig'
	'.git-completion.bash'
) 

for i in ${filenames[@]}; do
	cp -i -R ${i} ~/
	cp -i ${i} ~/
done

exit 0
