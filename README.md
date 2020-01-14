# Installation instructions

1. Install [Homebrew](https://brew.sh/), the package manager for macOS.
2. Use `Homebrew` to install [tmux](https://formulae.brew.sh/formula/tmux), [tmuxinator](https://formulae.brew.sh/formula/tmuxinator).
3. Set `vim` as default editor and install [vundle](https://github.com/VundleVim/Vundle.vim)
4. Get [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh/)(recommended).
5. Clone this repo and create symlinks
```bash
	$ git clone https://github.com/adilansari/dot_files.git
	$ sh dot_files/install.sh
```
6. Change the terminal theme to material-shell:
	- Terminal -> Preferences -> Profiles
	- Expand the Settings icon at the bottom of list of themes in left sidebar
	- Import the `$DOT_FILES_DIR/osx/materialshell-dark.terminal` theme and set as Default.
	- Restart terminal
7. [Install Vim plugins](https://github.com/VundleVim/Vundle.vim/blob/v0.10.2/doc/vundle.txt#L234-L254)
	- Open vimrc, `vi $HOME/.vimrc`
	- `:PluginInstall`

> `install.sh` file creates symlinks to the needed files.

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
| :art: | [gitmoji-cli](https://github.com/carloscuesta/gitmoji-cli) | improving the **look** of git commits |
| :speaker: | [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh) | **Shell** works best |
| :sparkles: | [IntelliJ material theme](https://plugins.jetbrains.com/plugin/8006-material-theme-ui) | IntelliJ UI theme |
| :elephant: | [httpie](https://httpie.org/) | beautiful **CuRL** replacement with goodies  |
| :dolphin: | [autojump](https://github.com/wting/autojump) | **cd** command but fast |
| :snake: | [hack](http://sourcefoundry.org/hack/) | beautiful **fontface** for source code |
| :ribbon: | [ctop](https://bcicen.github.io/ctop/) | top like **container metrics** |


# License
```
The MIT License

Copyright (c) 2016 Adil Ansari

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
