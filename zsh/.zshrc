# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# Path to your oh-my-zsh installation.
export ZSH=$HOME/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
#ZSH_THEME="materialshell-dark"

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
ENABLE_CORRECTION="false"

# Uncomment the following line to display red dots whilst waiting for completion.
COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
ZSH_CUSTOM=$HOME/.zsh/custom

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(autojump git python history history-substring-search colorize command-not-found tmux)


# User configuration

export EDITOR='nvim'

source $ZSH/oh-my-zsh.sh
source $HOME/.zsh/tmuxinator.zsh
# since we are using powerlevel10k prompts, this is redundant
# source $HOME/.zsh/prompts.zsh
source $HOME/.zsh/functions.zsh
source $HOME/.zsh/aliases

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# go path
export GOPATH="$HOME/devbox/gocode"
export GOBIN="$GOPATH/bin"
export PATH="$PATH:$GOPATH:$GOBIN:$HOME/.local/bin"
export PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH"
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
# Add RVM to PATH for scripting. Make sure this is the last PATH variable change.
export PATH="$PATH:$HOME/.rvm/bin"

# Only load p10k if not in Cursor/IDE and not already loaded
if [[ -n "$TERM_PROGRAM" ]] && [[ "$TERM_PROGRAM" == "cursor" ]] || [[ -n "$VSCODE_INJECTION" ]]; then
  # Simple prompt for Cursor to ensure clean output parsing
  PROMPT='%~ %# '
else
  # Load Powerlevel10k for regular terminals
  if [[ -z "$POWERLEVEL9K_VERSION" ]]; then
    source /opt/homebrew/share/powerlevel10k/powerlevel10k.zsh-theme
    # To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
    [[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh
  fi
fi

# Properly handle zsh-syntax-highlighting re-sourcing
if [[ -n "$ZSH_HIGHLIGHT_VERSION" ]]; then
  # Already loaded - clean up existing widgets to prevent recursion
  for widget in ${(k)widgets}; do
    if [[ "$widgets[$widget]" == user:_zsh_highlight_widget_* ]]; then
      zle -N $widget ${widgets[$widget]#user:_zsh_highlight_widget_}
    fi
  done
  unset ZSH_HIGHLIGHT_VERSION
  unfunction _zsh_highlight 2>/dev/null
  unfunction _zsh_highlight_bind_widgets 2>/dev/null
fi
export PATH="$PATH:$GOPATH:$GOBIN"

