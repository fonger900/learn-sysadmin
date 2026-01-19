---
title: 2. File Permissions
date: 2026-01-20
order: 2
---
# File Permissions

Linux uses a permission system to secure files.
Use `ls -l` to see permissions.

Example output: `-rwxr-xr--`

## Decoding Permissions
Broken into 3 sets of 3 characters:
1. **User (Owner)**: `rwx`
2. **Group**: `r-x`
3. **Others**: `r--`

- `r` (Read): 4
- `w` (Write): 2
- `x` (Execute): 1

## Changing Permissions (`chmod`)
- `chmod 755 file`: User(7=4+2+1), Group(5=4+1), Others(5=4+1)
- `chmod +x file`: Add execute permission for everyone
- `chmod u+w file`: Add write permission for user

## Changing Ownership (`chown`)
- `chown user:group file`: Change owner and group
- `chown user file`: Change owner only
- `chown :group file`: Change group only
