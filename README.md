# Installation instructions

1. Install [Homebrew](https://brew.sh/), the package manager for macOS.
2. Clone this repo and run the installer:
```bash
git clone https://github.com/adilansari/dot_files.git ~/onebox/dot_files
~/onebox/dot_files/install.sh
```
3. Install [nvchad](https://nvchad.com/docs/quickstart/install), then run `dots sync` to link the nvim files.
4. Change the terminal theme to material-shell:
	- Terminal -> Preferences -> Profiles
	- Expand the Settings icon at the bottom of list of themes in left sidebar
	- Import the `osx/materialshell-dark.terminal` theme and set as Default.
    - Change font to **Jetbrains Mono Nerd Font**, size: 16
	- Restart terminal

## What the installer does

The first run asks two questions and saves the answers in `~/.config/dotfiles/profile`:

| Question | Choices | Controls |
|---|---|---|
| Profile | `personal`, `work` | `packages/Brewfile` is always installed. The `personal` profile adds `Brewfile.personal`. Work packages live in the overlay, not in this repo. The profile also picks the matching files in `zsh/profiles` and `git/profiles`. |
| Private overlay | a folder path, a git URL, or empty | Machine-specific config that does not belong in this repo |

Then it installs the Homebrew packages, clones oh-my-zsh and tpm if they are missing, and links the config files into your home folder. Files that were already there are moved to `~/.local/state/dotfiles/backup/`.

To skip the questions, for example on a server:
```bash
PROFILE=personal OVERLAY= ~/onebox/dot_files/install.sh
```

## Daily use

| Command | What it does |
|---|---|
| `dots status` | Git status of this repo and the overlay |
| `dots sync` | Pull, then run the installer again |
| `dots doctor` | List links that are missing or were replaced by a real file |

## Private overlay

An overlay is a folder with its own `install.sh`. It keeps machine-specific config out of this repo. It can add files at these points:

| Tool | Overlay file |
|---|---|
| zsh | `~/.config/zsh/conf.d/*.zsh` |
| git | `~/.config/git/local.gitconfig` |
| tmux | `~/.config/tmux/local.conf` |
| tmuxinator | `~/.tmuxinator/<name>.yml` |
| gh-dash | `~/.config/gh-dash/config.yml` |
| Claude Code | `~/.claude/rules/*.md`, `~/.claude/skills/<name>` |

A minimal overlay `install.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
here=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
source "$DOTFILES_DIR/lib/link.sh"
link "$here/zsh/overlay.zsh" "$HOME/.config/zsh/conf.d/50-overlay.zsh"
```


# tmux + zsh = awesomeness

![powertools](https://raw.github.com/adilansari/.dot_files/master/screengrabs/terminal.png)

# Vim

### What it looks like now?
![Terminal mode (_No GUI_)](https://raw.github.com/adilansari/.dot_files/master/screengrabs/vimrc.png)

# Scores in status bar

`.tmux.conf` runs for `($HOME/.tmux-status.sh)` in your home directory, create that executable file and status bar will display the string output of that executable.

This is how my `($HOME/.tmux-status.sh)` executable file looks like to display cricket/soccer scores:
```
#!/bin/bash
cd $HOME/dot_files/tmux/statusbar-scripts
env/bin/python scores.py [API_SECRET]
```
> Note: I have a python virtualenv created in that directory.

![Cricket score in tmux status bar](https://raw.github.com/adilansari/.dot_files/master/tmux/statusbar-scripts/screengrabs/cric-score.png)

# Other installations

----------------

| Emoji | What | Description |
|:---:|:---:|---|
| :speaker: | [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) | **Shell** works best |
| :elephant: | [httpie](https://httpie.org/) | beautiful **CuRL** replacement with goodies  |
| :roller_coaster: | [zoxide](https://github.com/ajeetdsouza/zoxide) | **cd** command but fast |
| :snake: | [nerd fonts](https://www.nerdfonts.com/) | beautiful **fontfaces** for source code |
| :recycle: | [github dashboard](https://github.com/dlvhdr/gh-dash) | GitHub dashboard **on your terminal** |
| :file_folder: | [yazi](https://yazi-rs.github.io/) | **Terminal file manager** with vim-like keybindings |

[curated list of awesome CLIs](https://dlvhdr.me/posts/cli-tools)

# License
```
The MIT License

Copyright (c) 2026 Adil Ansari

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
