export PATH="usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin"
export TERM="xterm-256color"

#git autocomplete
if [ -f ~/.git-completion.bash ]; then
	  . ~/.git-completion.bash
fi

if [ -f ~/.zsh/aliases ]; then
	. ~/.zsh/aliases
fi
