# dot_files

Public dotfiles. One shared base, plus an optional private overlay per machine.

## Rules

- **This repo is public. Never add machine-specific or employer-specific data**: company or product names, private repo names, hostnames, cluster names, CI workflow names, internal paths, people's names, or non-public email addresses. This covers files, commit messages, branch names, PR text, and issues.
- That kind of data belongs in the private overlay (`OVERLAY_DIR` in `~/.config/dotfiles/profile`). Public files hold the logic and read the values from the overlay.
- The home folder links into this working tree, so it is live config. Do not stash, reset, or switch branches here without asking. Use a git worktree for larger changes.
- Scripts must run on bash 3.2 (the macOS default) and on Linux. Use `ln -s`, not `ln -sfh`.

## Layout

| Path | Purpose |
|---|---|
| `install.sh` | Asks the profile once, installs packages, creates links, runs the overlay |
| `lib/link.sh` | `link`, `link_each`, `check_links`. Overlays source it too. |
| `bin/dots` | `dots status`, `dots sync`, `dots doctor` |
| `.githooks/` | Block commits that match the overlay's blocklist |
| `packages/` | `Brewfile` (every machine), `Brewfile.personal`. Work packages are not public: they go in the overlay's `Brewfile`. |
| `zsh/profiles/<profile>.zsh` | Profile-only shell setup |
| `git/profiles/<profile>.gitconfig` | Profile-only git setup |

## Drop-in points for an overlay

| Tool | Overlay file |
|---|---|
| zsh | `~/.config/zsh/conf.d/*.zsh` |
| git | `~/.config/git/local.gitconfig` |
| tmux | `~/.config/tmux/local.conf` |
| tmuxinator | `~/.tmuxinator/<name>.yml` |
| gh-dash | `~/.config/gh-dash/config.yml` (replaces the public link) |
| Claude Code | `~/.claude/rules/*.md`, `~/.claude/skills/<name>` |

## Testing

Run the install against a throwaway home folder, never the real one:

```sh
HOME=$(mktemp -d) PROFILE=personal OVERLAY= ./install.sh --no-packages
```
