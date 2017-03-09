
# Setting PATH for Python 2.7

# The orginal version is saved in .bash_profile.pysave
#export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:${PATH}"
PYTHONPATH="/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/"
export PYTHONPATH

export JAVA_HOME=$(/usr/libexec/java_home)
export PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/texbin:/Users/adil/Code/adt-bundle-mac-x86_64-20140321/sdk/platform-tools"
export PATH=${PATH}:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin
export PATH=/usr/local/php5/bin:$HOME/.composer/vendor/bin:/usr/local/mysql/bin:$PATH
export TERM="xterm-256color"

#git autocomplete
if [ -f ~/.git-completion.bash ]; then
	  . ~/.git-completion.bash
fi

if [ -f ~/.zsh/aliases ]; then
	. ~/.zsh/aliases
fi


export NVM_DIR="/Users/adil.ansari/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"  # This loads nvm
