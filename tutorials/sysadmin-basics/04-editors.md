---
title: 4. Text Editors
date: 2026-01-20
order: 4
---
# Text Editors

As a system administrator, you'll spend significant time editing configuration files, scripts, and logs. Knowing a terminal-based text editor is essential—especially on servers without a graphical interface.

## Choosing an Editor

| Editor | Learning Curve | Best For |
|--------|----------------|----------|
| **nano** | Easy | Beginners, quick edits |
| **vim** | Steep | Power users, efficiency |
| **emacs** | Steep | Developers, extensibility |

## Nano - The Beginner-Friendly Editor

Nano is simple and intuitive. Commands are displayed at the bottom.

### Basic Usage
```bash
$ nano filename.txt       # Open or create file
```

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + O` | Save file (Write Out) |
| `Ctrl + X` | Exit nano |
| `Ctrl + K` | Cut current line |
| `Ctrl + U` | Paste (Uncut) |
| `Ctrl + W` | Search |
| `Ctrl + \` | Search and replace |
| `Ctrl + G` | Help |
| `Alt + A` | Start selection |
| `Ctrl + C` | Show cursor position |
| `Alt + U` | Undo |
| `Alt + E` | Redo |

### Navigation
| Shortcut | Action |
|----------|--------|
| `Ctrl + A` | Go to beginning of line |
| `Ctrl + E` | Go to end of line |
| `Ctrl + Y` | Page up |
| `Ctrl + V` | Page down |
| `Alt + \` | Go to beginning of file |
| `Alt + /` | Go to end of file |
| `Ctrl + _` | Go to line number |

### Nano Configuration
Create `~/.nanorc` for customization:
```bash
set linenumbers       # Show line numbers
set tabsize 4         # Tab = 4 spaces
set autoindent        # Auto-indent new lines
set mouse             # Enable mouse support
include "/usr/share/nano/*.nanorc"  # Syntax highlighting
```

## Vim - The Power Editor

Vim is a modal editor—it has different modes for different tasks. This design enables incredibly fast editing once mastered.

### Vim Modes

```
┌─────────────────────────────────────────────┐
│                NORMAL MODE                  │
│           (Navigation, commands)            │
│                                             │
│    i, a, o          ──────►  INSERT MODE    │
│                              (Type text)    │
│    ◄──────          Esc                     │
│                                             │
│    v, V, Ctrl+v    ──────►  VISUAL MODE     │
│                              (Selection)    │
│    ◄──────          Esc                     │
│                                             │
│    :               ──────►  COMMAND MODE    │
│                              (:w, :q, etc)  │
│    ◄──────          Enter/Esc               │
└─────────────────────────────────────────────┘
```

| Mode | Purpose | How to Enter |
|------|---------|--------------|
| **Normal** | Navigation, commands | `Esc` (default mode) |
| **Insert** | Typing text | `i`, `a`, `o`, `I`, `A`, `O` |
| **Visual** | Selecting text | `v`, `V`, `Ctrl+v` |
| **Command** | Ex commands | `:` |

### Entering Insert Mode

| Key | Action |
|-----|--------|
| `i` | Insert before cursor |
| `a` | Append after cursor |
| `I` | Insert at beginning of line |
| `A` | Append at end of line |
| `o` | Open new line below |
| `O` | Open new line above |

### Navigation (Normal Mode)

| Key | Action |
|-----|--------|
| `h`, `j`, `k`, `l` | Left, Down, Up, Right |
| `w` | Next word |
| `b` | Back one word |
| `0` | Beginning of line |
| `$` | End of line |
| `gg` | Go to first line |
| `G` | Go to last line |
| `5G` or `:5` | Go to line 5 |
| `Ctrl + f` | Page down |
| `Ctrl + b` | Page up |
| `%` | Jump to matching bracket |

### Editing (Normal Mode)

| Key | Action |
|-----|--------|
| `x` | Delete character |
| `dd` | Delete line |
| `dw` | Delete word |
| `d$` or `D` | Delete to end of line |
| `yy` | Yank (copy) line |
| `yw` | Yank word |
| `p` | Paste after cursor |
| `P` | Paste before cursor |
| `u` | Undo |
| `Ctrl + r` | Redo |
| `.` | Repeat last command |

### Search and Replace

| Command | Action |
|---------|--------|
| `/pattern` | Search forward |
| `?pattern` | Search backward |
| `n` | Next match |
| `N` | Previous match |
| `:%s/old/new/g` | Replace all in file |
| `:s/old/new/g` | Replace all in line |
| `:%s/old/new/gc` | Replace with confirmation |

### Saving and Quitting (Command Mode)

| Command | Action |
|---------|--------|
| `:w` | Save (write) |
| `:q` | Quit |
| `:wq` or `:x` | Save and quit |
| `:q!` | Quit without saving |
| `:w filename` | Save as new file |
| `ZZ` | Save and quit (Normal mode) |

### Vim Configuration
Create `~/.vimrc` for customization:
```vim
set number            " Show line numbers
set relativenumber    " Relative line numbers
set tabstop=4         " Tab = 4 spaces
set shiftwidth=4      " Indent = 4 spaces
set expandtab         " Use spaces instead of tabs
set autoindent        " Auto-indent new lines
set hlsearch          " Highlight search results
set incsearch         " Incremental search
syntax on             " Syntax highlighting
set mouse=a           " Enable mouse
```

## Quick Reference Card

### If you're stuck in Vim:
1. Press `Esc` (maybe twice)
2. Type `:q!` and press `Enter`

### Nano Survival:
- `Ctrl + O` → Save
- `Ctrl + X` → Exit

### Vim Survival:
- `i` → Start typing
- `Esc` → Stop typing
- `:wq` → Save and quit

## Hands-On Exercise

1. Practice with nano:
   ```bash
   $ nano practice.txt
   # Type some text
   # Save with Ctrl+O
   # Exit with Ctrl+X
   ```

2. Set the default editor:
   ```bash
   $ export EDITOR=vim    # or nano
   $ echo "export EDITOR=vim" >> ~/.bashrc
   ```

3. Practice Vim basics:
   ```bash
   $ vim practice.txt
   # Press i, type text
   # Press Esc
   # Type :wq to save and exit
   ```

4. Try Vim navigation:
   ```bash
   $ vim /etc/passwd
   # Use j/k to move up/down
   # Use gg and G to jump
   # Use /root to search
   # Exit with :q
   ```

5. Master one editor by editing your shell config:
   ```bash
   $ vim ~/.bashrc    # or nano ~/.bashrc
   # Add: alias ll='ls -la'
   # Save and exit
   $ source ~/.bashrc
   $ ll
   ```
