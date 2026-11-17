#!/usr/bin/env bash
set -euo pipefail

DOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CONFIG_DIR=${XDG_CONFIG_HOME:-$HOME/.config}
STATE_FILE=$CONFIG_DIR/dotfiles/profile

# shellcheck source=lib/link.sh
source "$DOT/lib/link.sh"

usage() {
  cat <<EOF
usage: install.sh [--check] [--no-packages]

  --check        report links that are missing, replaced, or dangling
  --no-packages  skip Homebrew packages and third-party clones

First run asks for a profile. To skip the questions, set:
  PROFILE=personal|work  OVERLAY=<path or git URL, may be empty>
To ask again, delete $STATE_FILE
EOF
}

load_profile() {
  if [[ -f $STATE_FILE ]]; then
    # shellcheck source=/dev/null
    source "$STATE_FILE"
    return
  fi

  [[ -n ${PROFILE:-} ]] || read -rp "Profile (personal/work): " PROFILE
  [[ -n ${OVERLAY+set} ]] || read -rp "Private overlay, path or git URL (empty for none): " OVERLAY

  case $PROFILE in
    personal|work) ;;
    *) echo "unknown profile: $PROFILE" >&2; exit 2 ;;
  esac

  OVERLAY=${OVERLAY/#\~/$HOME}
  if [[ -z $OVERLAY ]]; then
    OVERLAY_DIR=
  elif [[ -d $OVERLAY ]]; then
    OVERLAY_DIR=$(cd "$OVERLAY" && pwd)
  else
    OVERLAY_DIR=${XDG_DATA_HOME:-$HOME/.local/share}/dotfiles-overlay
  fi

  mkdir -p "$(dirname "$STATE_FILE")"
  printf 'PROFILE=%q\nOVERLAY=%q\nOVERLAY_DIR=%q\n' \
    "$PROFILE" "$OVERLAY" "$OVERLAY_DIR" > "$STATE_FILE"
}

clone_if_missing() {
  local url=$1 dir=$2
  if [[ ! -d $dir ]]; then
    git clone --depth 1 "$url" "$dir"
  fi
}

install_packages() {
  local f
  case $(uname -s) in
    Darwin)
      if ! command -v brew >/dev/null; then
        echo "Homebrew is not installed. Install it from https://brew.sh and run this again." >&2
        exit 1
      fi
      for f in Brewfile "Brewfile.$PROFILE"; do
        if [[ -f $DOT/packages/$f ]]; then
          brew bundle --no-upgrade --file="$DOT/packages/$f"
        fi
      done
      ;;
    Linux)
      if [[ -x $DOT/packages/linux.sh ]]; then
        "$DOT/packages/linux.sh" "$PROFILE"
      fi
      ;;
  esac

  clone_if_missing https://github.com/ohmyzsh/ohmyzsh.git "$HOME/.oh-my-zsh"
  clone_if_missing https://github.com/tmux-plugins/tpm.git "$HOME/.tmux/plugins/tpm"
}

link_base() {
  link "$DOT/zsh/.zsh"                 "$HOME/.zsh"
  link "$DOT/zsh/.zshrc"               "$HOME/.zshrc"
  link "$DOT/zsh/.zsh/.p10k.zsh"       "$HOME/.p10k.zsh"
  link "$DOT/vim/.vimrc"               "$HOME/.vimrc"
  link "$DOT/tmux/.tmux.conf"          "$HOME/.tmux.conf"
  link "$DOT/tmux/scripts"             "$HOME/.tmux-scripts"
  link "$DOT/git/.git-completion.bash" "$HOME/.git-completion.bash"
  link "$DOT/git/.gitconfig"           "$HOME/.gitconfig"
  link "$DOT/git/.gitignore"           "$HOME/.gitignore"
  link "$DOT/.bash_profile"            "$HOME/.bash_profile"
  link "$DOT/claude/CLAUDE.md"         "$HOME/.claude/CLAUDE.md"
  link "$DOT/bin/dots"                  "$HOME/.local/bin/dots"

  link_each "$DOT/tmux/.tmuxinator" "$HOME/.tmuxinator"
  link_each "$DOT/config/gh-dash"   "$CONFIG_DIR/gh-dash"
  link_each "$DOT/claude/skills"    "$HOME/.claude/skills"
  link_each "$DOT/claude/hooks"     "$HOME/.claude/hooks"

  # NvChad owns ~/.config/nvim; creating the folder first would block its installer.
  if [[ -d $CONFIG_DIR/nvim/lua ]]; then
    link "$DOT/config/nvim/mappings.lua" "$CONFIG_DIR/nvim/lua/mappings.lua"
    link "$DOT/config/nvim/options.lua"  "$CONFIG_DIR/nvim/lua/options.lua"
  else
    echo "skipped nvim files: $CONFIG_DIR/nvim/lua not found (install NvChad, then run: dots sync)"
  fi
}

link_profile() {
  local f=$DOT/zsh/profiles/$PROFILE.zsh
  if [[ -f $f ]]; then
    link "$f" "$CONFIG_DIR/zsh/conf.d/10-profile.zsh"
  fi
  f=$DOT/git/profiles/$PROFILE.gitconfig
  if [[ -f $f ]]; then
    link "$f" "$CONFIG_DIR/git/profile.gitconfig"
  fi
}

# Claude Code rewrites settings.json itself, so it is patched in place and never linked.
patch_claude_settings() {
  local settings=$HOME/.claude/settings.json tmp
  if ! command -v jq >/dev/null; then
    echo "skipped Claude hook registration: jq not found"
    return 0
  fi
  [[ -f $settings ]] || echo '{}' > "$settings"
  if grep -q 'comment-audit.sh' "$settings"; then
    return 0
  fi
  tmp=$(mktemp)
  if jq '.hooks.PostToolUse += [{"matcher":"Edit|Write|MultiEdit","hooks":[{"type":"command","command":"sh \"$HOME/.claude/hooks/comment-audit.sh\""}]}]' "$settings" > "$tmp"; then
    mv "$tmp" "$settings"
    echo "registered comment-audit hook in $settings"
  else
    rm -f "$tmp"
    echo "WARN: could not patch $settings (invalid JSON?), left unchanged" >&2
  fi
}

configure_repo() {
  git -C "$DOT" config user.email "$(git config -f "$DOT/git/.gitconfig" user.email)"
  git -C "$DOT" config core.hooksPath .githooks
}

install_overlay() {
  if [[ -z $OVERLAY_DIR ]]; then
    return 0
  fi
  if [[ ! -d $OVERLAY_DIR ]] && ! git clone "$OVERLAY" "$OVERLAY_DIR"; then
    echo "could not clone the overlay. Log in to the git host, then run: dots sync" >&2
    return 1
  fi
  if [[ ! -x $OVERLAY_DIR/install.sh ]]; then
    echo "overlay has no executable install.sh: $OVERLAY_DIR" >&2
    return 1
  fi
  DOTFILES_DIR=$DOT DOTFILES_NO_PACKAGES=$no_packages "$OVERLAY_DIR/install.sh"
}

check=0
no_packages=
for arg in "$@"; do
  case $arg in
    --check) check=1 ;;
    --no-packages) no_packages=1 ;;
    -h|--help) usage; exit 0 ;;
    *) usage >&2; exit 2 ;;
  esac
done

if (( check )); then
  check_links
  exit 0
fi

load_profile
export DOTFILES_OVERLAY_DIR=$OVERLAY_DIR
echo "profile: $PROFILE, overlay: ${OVERLAY_DIR:-none}"

if [[ -z $no_packages ]]; then
  install_packages
fi

mkdir -p "$DOTFILES_STATE_DIR"
: > "$DOTFILES_LINKS_FILE"

link_base
link_profile
patch_claude_settings
configure_repo
install_overlay

echo "done. Open a new shell to load the changes."
