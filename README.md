# Install

- Install [tmux](http://linoxide.com/how-tos/install-tmux-manage-multiple-linux-terminals/)(optional).
- But you definitely need [vim](http://www.vim.org/download.php) and [Vundle](https://github.com/VundleVim/Vundle.vim), its a package manager for vim.
- If you clone this repo in your **$HOME** directory.

```bash
	$ git clone https://github.com/adilansari/dot_files.git
	$ cd dot_files
	$ ./install.sh
```

- Else update the `dot_files_dir` in the **install.sh** file to the location where this is cloned and follow the above steps.

> `install.sh` file creates symlinks to the needed files.

# tmux + zsh = awesomeness
=======
![powertools](https://raw.github.com/adilansari/.dot_files/master/screengrabs/terminal.png)

# Vim
=======
### What it looks like now?
![Terminal mode (_No GUI_)](https://raw.github.com/adilansari/.dot_files/master/screengrabs/vimrc.png)

# Cricket Score
=======
![Cricket score in tmux status bas](https://raw.github.com/adilansari/.dot_files/master/tmux/statusbar-scripts/screengrabs/cric-score.png)

# Suggested Improvements
- Lemme start using emojis in commit mesages

Suggested Emojis
----------------

| Emoji | Raw Emoji Code | Description |
|:---:|:---:|---|
| :art: | `:art:` | when improving the **format**/structure of the code |
| :racehorse: | `:racehorse:` | when improving **performance** |
| :books: | `:books:` | when writing **docs** |
| :bug: | `:bug:` | when reporting a **bug**, with [`@FIXME`](https://github.com/slashsBin/styleguide-todo-grammar#bug-report)Comment Tag |
| :ambulance: | `:ambulance:` | when fixing a **bug** |
| :penguin: | `:penguin:` | when fixing something on **Linux** |
| :apple: | `:apple:` | when fixing something on **Mac OS** |
| :checkered_flag: | `:checkered_flag:` | when fixing something on **Windows** |
| :fire: | `:fire:` | when **removing code** or files, _maybe_ with `@CHANGED` Comment Tag |
| :umbrella: | `:umbrella:` | when adding **tests** |
| :green_heart: | `:green_heart:` | when fixing the **CI** build |
| :lock: | `:lock:` | when dealing with **security** |
| :arrow_up: | `:arrow_up:` | when upgrading **dependencies** |
| :arrow_down: | `:arrow_down:` | when downgrading **dependencies** |
| :fast_forward: | `:fast_forward:` | when **forward-porting features** from an older version/branch |
| :rewind: | `:rewind:` | when **backporting features** from a newer version/branch |
| :shirt: | `:shirt:` | when removing **linter**/strict/deprecation warnings |
| :lipstick: | `:lipstick:` | when improving **UI**/Cosmetic |
| :wheelchair: | `:wheelchair:` | when improving **accessibility** |
| :globe_with_meridians: | `:globe_with_meridians:` | when dealing with **globalization**/internationalization/i18n/g11n |
| :construction: | `:construction:` | **WIP**(Work In Progress) Commits, _maybe_ with `@REVIEW` Comment Tag |
| :gem: | `:gem:` | New **Release** |
| :bookmark: | `:bookmark:` | Version **Tags** |
| :tada: | `:tada:` | **Initial** Commit |
| :speaker: | `:speaker:` | when Adding **Logging** |
| :mute: | `:mute:` | when Reducing **Logging** |
| :sparkles: | `:sparkles:` | when introducing **New** Features |
| :zap: | `:zap:` | when introducing **Backward-InCompatible** Features, _maybe_ with `@CHANGED` Comment Tag |
| :bulb: | `:bulb:` | New **Idea**, with `@IDEA` Comment Tag |
| :snowflake: | `:snowflake:` | changing **Configuration**, Usually together with :penguin: or :ribbon: or :rocket: |
| :ribbon: | `:ribbon:` | Customer requested application **Customization**, with `@HACK` Comment Tag |
| :rocket: | `:rocket:` | Anything related to Deployments/**DevOps** |
| :elephant: | `:elephant:` | **PostgreSQL** Database specific(Migrations, Scripts, Extensions, ...)  |
| :dolphin: | `:dolphin:` | **MySQL** Database specific(Migrations, Scripts, Extensions, ...) |

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
