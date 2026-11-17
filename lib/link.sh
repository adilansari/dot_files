# shellcheck shell=bash

DOTFILES_STATE_DIR=${XDG_STATE_HOME:-$HOME/.local/state}/dotfiles
DOTFILES_LINKS_FILE=$DOTFILES_STATE_DIR/links
DOTFILES_BACKUP_DIR=$DOTFILES_STATE_DIR/backup/$(date +%Y%m%d-%H%M%S)

record_link() {
  mkdir -p "$DOTFILES_STATE_DIR"
  printf '%s\t%s\n' "$2" "$1" >> "$DOTFILES_LINKS_FILE"
}

link() {
  local src=$1 dst=$2 parent current overlay=${DOTFILES_OVERLAY_DIR:-}
  parent=$(dirname "$dst")

  if [[ ! -e $src ]]; then
    echo "missing source: $src" >&2
    return 1
  fi
  # Writing through a symlinked parent would create the link inside another repo's folder.
  if [[ -L $parent ]]; then
    echo "refusing to link $dst: $parent is a symlink" >&2
    return 1
  fi

  if [[ -L $dst ]]; then
    current=$(readlink "$dst")
    if [[ $current == "$src" ]]; then
      record_link "$src" "$dst"
      return 0
    fi
    # The overlay replaces some public links; relinking them here would flip them on every run.
    if [[ -n $overlay && $current == "$overlay"/* && $src != "$overlay"/* && -e $current ]]; then
      return 0
    fi
    rm "$dst"
  elif [[ -e $dst ]]; then
    mkdir -p "$DOTFILES_BACKUP_DIR$parent"
    mv "$dst" "$DOTFILES_BACKUP_DIR$dst"
    echo "backed up $dst to $DOTFILES_BACKUP_DIR$dst"
  fi

  mkdir -p "$parent"
  ln -s "$src" "$dst"
  record_link "$src" "$dst"
  echo "linked $dst"
}

link_each() {
  local src_dir=$1 dst_dir=$2 entry target

  if [[ -L $dst_dir ]]; then
    echo "replacing folder link $dst_dir with a real folder"
    rm "$dst_dir"
  fi
  mkdir -p "$dst_dir"

  for entry in "$dst_dir"/*; do
    [[ -L $entry ]] || continue
    target=$(readlink "$entry")
    if [[ $target == "$src_dir"/* && ! -e $target ]]; then
      echo "removing stale link $entry"
      rm "$entry"
    fi
  done

  for entry in "$src_dir"/*; do
    [[ -e $entry ]] || continue
    link "$entry" "$dst_dir/$(basename "$entry")"
  done
}

check_links() {
  local dst src bad=0

  if [[ ! -f $DOTFILES_LINKS_FILE ]]; then
    echo "no links recorded yet, run install.sh first" >&2
    return 1
  fi

  while IFS=$'\t' read -r dst src; do
    if [[ ! -L $dst ]]; then
      echo "not a link: $dst (expected -> $src)"
      bad=1
    elif [[ $(readlink "$dst") != "$src" ]]; then
      echo "wrong target: $dst -> $(readlink "$dst") (expected $src)"
      bad=1
    elif [[ ! -e $src ]]; then
      echo "dangling: $dst -> $src"
      bad=1
    fi
  done < <(awk -F'\t' '{ last[$1] = $2 } END { for (d in last) print d "\t" last[d] }' "$DOTFILES_LINKS_FILE" | sort)

  if (( bad == 0 )); then
    echo "all links ok"
  fi
  return $bad
}
