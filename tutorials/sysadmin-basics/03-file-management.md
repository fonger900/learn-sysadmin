---
title: 3. File Management
date: 2026-01-20
order: 3
---
# File Management

Mastering file operations is fundamental to system administration. This tutorial covers creating, copying, moving, deleting files, and powerful tools for finding and manipulating them.

## Creating Files and Directories

### Creating Files
```bash
$ touch newfile.txt           # Create empty file (or update timestamp)
$ echo "Hello" > file.txt     # Create file with content
$ cat > notes.txt             # Type content, Ctrl+D to save
```

### Creating Directories
```bash
$ mkdir projects              # Create single directory
$ mkdir -p a/b/c              # Create nested directories
$ mkdir -m 700 private        # Create with specific permissions
```

## Copying Files and Directories

| Command | Description |
|---------|-------------|
| `cp file1 file2` | Copy file1 to file2 |
| `cp file dir/` | Copy file into directory |
| `cp -r dir1 dir2` | Copy directory recursively |
| `cp -i file dest` | Interactive (prompt before overwrite) |
| `cp -p file dest` | Preserve permissions and timestamps |
| `cp -v file dest` | Verbose (show what's being copied) |

```bash
$ cp config.txt config.bak              # Backup a file
$ cp -r /etc/nginx /backup/             # Copy entire directory
$ cp -rp /home/user /backup/            # Preserve ownership
```

## Moving and Renaming

The `mv` command moves **and** renames files:

```bash
$ mv oldname.txt newname.txt            # Rename file
$ mv file.txt ~/Documents/              # Move to directory
$ mv dir1 dir2                          # Rename directory
$ mv -i important.txt /backup/          # Prompt before overwrite
$ mv -v *.log /var/log/archive/         # Move with verbose output
```

## Deleting Files and Directories

> **WARNING**: Linux has no recycle bin. Deleted files are gone forever!

| Command | Description |
|---------|-------------|
| `rm file` | Remove file |
| `rm -r dir` | Remove directory recursively |
| `rm -f file` | Force (no prompts) |
| `rm -i file` | Interactive (confirm each) |
| `rmdir dir` | Remove empty directory only |

```bash
$ rm unwanted.txt                       # Delete file
$ rm -r old_project/                    # Delete directory
$ rm -rf /tmp/cache/*                   # Force delete contents
$ rmdir empty_folder                    # Only works if empty
```

**Safety tip**: Use `rm -i` or alias `rm` to `rm -i` for protection.

## Viewing File Contents

| Command | Description | Best For |
|---------|-------------|----------|
| `cat file` | Output entire file | Small files |
| `less file` | Paginated viewer | Large files |
| `head file` | First 10 lines | Quick peek |
| `tail file` | Last 10 lines | Log files |
| `tail -f file` | Follow new lines | Live monitoring |
| `more file` | Basic pager | Legacy systems |

```bash
$ cat /etc/hostname
$ less /var/log/syslog              # Use q to quit
$ head -20 /var/log/auth.log        # First 20 lines
$ tail -50 /var/log/nginx/access.log
$ tail -f /var/log/syslog           # Watch live (Ctrl+C to stop)
```

## Wildcards (Globbing)

Wildcards let you match multiple files with patterns:

| Pattern | Matches | Example |
|---------|---------|---------|
| `*` | Any characters (0 or more) | `*.txt` → all .txt files |
| `?` | Exactly one character | `file?.txt` → file1.txt |
| `[abc]` | One of the characters | `file[123].txt` |
| `[a-z]` | Range of characters | `[A-Z]*.log` |
| `[!abc]` | Not these characters | `file[!0-9].txt` |

```bash
$ ls *.log                    # All log files
$ rm temp?.txt                # temp1.txt, temp2.txt, etc.
$ cp config[0-9].conf /backup/
$ mv *2024* archive/          # Files containing "2024"
```

## Finding Files

### The `find` Command
Powerful, searches in real-time:

```bash
# By name
$ find /home -name "*.txt"
$ find /etc -name "*.conf" -type f

# By type
$ find /var -type d -name "log*"     # Directories only
$ find /home -type f -size +100M     # Files over 100MB

# By time
$ find /tmp -mtime +7                # Modified 7+ days ago
$ find /var/log -mmin -60            # Modified in last 60 minutes

# Execute action
$ find /tmp -name "*.tmp" -delete
$ find . -name "*.bak" -exec rm {} \;
```

### The `locate` Command
Fast, uses database (run `updatedb` to refresh):

```bash
$ locate nginx.conf
$ locate -i README              # Case insensitive
$ locate -c "*.py"              # Count matches
```

## Text Processing Tools

| Command | Description |
|---------|-------------|
| `wc` | Count lines, words, characters |
| `sort` | Sort lines |
| `uniq` | Remove duplicate lines |
| `cut` | Extract columns |
| `grep` | Search for patterns |

```bash
$ wc -l /etc/passwd              # Count lines (users)
$ sort names.txt                 # Sort alphabetically
$ sort -n numbers.txt            # Sort numerically
$ cat file.txt | sort | uniq     # Unique lines only
$ cut -d: -f1 /etc/passwd        # Extract usernames
$ grep "error" /var/log/syslog   # Find lines with "error"
$ grep -r "TODO" ~/projects/     # Recursive search
```

## Linking Files

### Hard Links
Same file, different name (same inode):
```bash
$ ln original.txt hardlink.txt
$ ls -li    # Same inode number
```

### Symbolic Links (Symlinks)
Pointer to another file (like a shortcut):
```bash
$ ln -s /path/to/original symlink
$ ln -s /usr/bin/python3 /usr/bin/python
$ ls -l    # Shows -> pointing to target
```

## Hands-On Exercise

1. Create a project structure:
   ```bash
   $ mkdir -p myproject/{src,docs,tests}
   $ touch myproject/README.md
   $ touch myproject/src/main.py
   ```

2. Practice copying and moving:
   ```bash
   $ cp myproject/README.md myproject/docs/
   $ mv myproject/src/main.py myproject/src/app.py
   ```

3. Use wildcards to list files:
   ```bash
   $ ls /etc/*.conf | head -5
   $ find /etc -name "*.conf" -type f | wc -l
   ```

4. Find large files on your system:
   ```bash
   $ find /var -type f -size +10M 2>/dev/null | head -10
   ```

5. Create and use a symlink:
   ```bash
   $ ln -s ~/myproject/docs ~/quick-docs
   $ ls -l ~/quick-docs
   ```
