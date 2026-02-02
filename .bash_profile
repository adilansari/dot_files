export PATH="usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin"
export TERM="xterm-256color"

#git autocomplete
if [ -f ~/.git-completion.bash ]; then
	  . ~/.git-completion.bash
fi

if [ -f ~/.zsh/aliases ]; then
	. ~/.zsh/aliases
fi

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
