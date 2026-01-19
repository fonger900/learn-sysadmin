---
title: 1. Terminal Basics
date: 2026-01-20
order: 1
---
# Terminal Basics

The terminal is your primary tool as a system administrator. Mastering the command line allows you to work faster, automate tasks, and manage remote servers efficiently.

## What is a Shell?

A **shell** is a program that interprets your commands and communicates with the operating system. Think of it as a translator between you and the Linux kernel.

| Shell | Description | Config File |
|-------|-------------|-------------|
| **bash** | Bourne Again Shell, default on most Linux | `~/.bashrc` |
| **zsh** | Z Shell, default on macOS, feature-rich | `~/.zshrc` |
| **sh** | Original Bourne Shell, minimal | `~/.profile` |
| **fish** | Friendly Interactive Shell | `~/.config/fish/config.fish` |

Check your current shell:
```bash
$ echo $SHELL
/bin/bash
```

## Opening the Terminal

| Desktop Environment | Shortcut |
|---------------------|----------|
| GNOME / Ubuntu | `Ctrl` + `Alt` + `T` |
| KDE Plasma | `Ctrl` + `Alt` + `T` |
| macOS | `Cmd` + `Space`, type "Terminal" |
| Windows (WSL) | Search "Ubuntu" or "WSL" |

## Understanding the Prompt

When you open a terminal, you'll see a prompt like this:
```
user@hostname:~$
```

| Part | Meaning |
|------|---------|
| `user` | Your current username |
| `hostname` | The machine's name |
| `~` | Current directory (`~` = home directory) |
| `$` | Standard user prompt |
| `#` | Root user prompt (superuser) |

## Command Structure

Every command follows this pattern:
```
command [options] [arguments]
```

**Examples:**
```bash
$ ls                    # command only
$ ls -l                 # command + option
$ ls -l /var/log        # command + option + argument
$ ls -la /var/log       # combined options (-l and -a)
```

## Essential Navigation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `pwd` | Print Working Directory | `pwd` → `/home/user` |
| `ls` | List directory contents | `ls -la` |
| `cd` | Change Directory | `cd /var/log` |
| `cd ~` | Go to home directory | `cd ~` or just `cd` |
| `cd ..` | Go up one directory | `cd ..` |
| `cd -` | Go to previous directory | `cd -` |

## Keyboard Shortcuts

These shortcuts dramatically speed up your workflow:

### Line Editing
| Shortcut | Action |
|----------|--------|
| `Ctrl + A` | Move cursor to beginning of line |
| `Ctrl + E` | Move cursor to end of line |
| `Ctrl + U` | Delete from cursor to beginning |
| `Ctrl + K` | Delete from cursor to end |
| `Ctrl + W` | Delete word before cursor |
| `Alt + B` | Move back one word |
| `Alt + F` | Move forward one word |

### History & Control
| Shortcut | Action |
|----------|--------|
| `Ctrl + R` | Reverse search command history |
| `Ctrl + C` | Cancel current command |
| `Ctrl + D` | Exit shell (or send EOF) |
| `Ctrl + L` | Clear screen (same as `clear`) |
| `↑` / `↓` | Navigate command history |
| `!!` | Repeat last command |
| `!$` | Last argument of previous command |

## Command History

Your shell remembers commands you've typed:

```bash
$ history           # Show command history
$ history 10        # Show last 10 commands
$ !123              # Run command #123 from history
$ !!                # Run the last command again
$ sudo !!           # Run last command with sudo
```

## Tab Completion

Press `Tab` to auto-complete commands, file names, and paths:
- **Single match**: Completes automatically
- **Multiple matches**: Press `Tab` twice to see options

```bash
$ cd /etc/sys<Tab>     # Completes to /etc/sysctl.d/
$ systemc<Tab><Tab>    # Shows: systemctl  systemd-...
```

## Aliases

Create shortcuts for frequently used commands:
```bash
# Add to ~/.bashrc or ~/.zshrc
alias ll='ls -la'
alias ..='cd ..'
alias update='sudo apt update && sudo apt upgrade'

# Reload config
$ source ~/.bashrc
```

View existing aliases:
```bash
$ alias
```

## Getting Help

| Method | Usage | Example |
|--------|-------|---------|
| `--help` | Quick help | `ls --help` |
| `man` | Full manual | `man ls` |
| `info` | Detailed docs | `info coreutils` |
| `whatis` | One-line description | `whatis ls` |
| `which` | Find command location | `which python` |

## Hands-On Exercise

1. Open your terminal and identify your shell:
   ```bash
   $ echo $SHELL
   ```

2. Navigate to your home directory and list all files (including hidden):
   ```bash
   $ cd ~
   $ ls -la
   ```

3. Practice the keyboard shortcuts:
   - Type a long command, then use `Ctrl + A` and `Ctrl + E`
   - Use `Ctrl + R` to search your history

4. Create an alias and test it:
   ```bash
   $ alias myip='curl ifconfig.me'
   $ myip
   ```

5. Use the manual to learn about a new command:
   ```bash
   $ man grep
   ```
