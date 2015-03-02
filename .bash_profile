
# Setting PATH for Python 2.7

# The orginal version is saved in .bash_profile.pysave
export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
export PATH=${PATH}:/Users/adil/Code/adt-bundle-mac-x86_64-20140321/sdk/platform-tools
export JAVA_HOME=$(/usr/libexec/java_home)
#export PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin
#export PATH=/usr/local/bin:$PATH
export TERM="xterm-256color"

#git autocomplete
if [ -f ~/.git-completion.bash ]; then
	  . ~/.git-completion.bash
fi

#bash aliases
alias ll='ls -la'

# git aliases
alias g='git status'
alias gad='git add'
alias gco='git checkout'
alias gcm='git commit'
alias glog='git log --oneline --graph'
alias gst='git stash'
alias gb='git branch'
alias gd='git diff'
alias greb='git rebase -i master'

# tmux aliases
alias tm='tmux at -t'

# ssh aliases
alias vagr='cd ~/onebox/ && vagrant ssh'
alias ssh_d='ssh adil@d.caffeine.io'

# ulimit for running grunt
ulimit -n 4096
