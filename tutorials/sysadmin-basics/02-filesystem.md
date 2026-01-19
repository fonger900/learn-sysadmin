---
title: 2. Filesystem Hierarchy
date: 2026-01-20
order: 2
---
# Linux Filesystem Hierarchy

Everything in Linux is a file. The filesystem starts at `/` (root).

## Key Directories

### `/bin` & `/sbin`
Essential command binaries. `/sbin` contains binaries for system administration (e.g., `reboot`, `fdisk`).

### `/etc`
Configuration files.
- `/etc/passwd`: User info
- `/etc/ssh/`: SSH configuration

### `/home`
User home directories (e.g., `/home/alice`).

### `/var`
Variable data like logs, caches, and spool files.
- `/var/log`: System logs

### `/tmp`
Temporary files. Cleared on reboot.

### `/root`
Home directory for the root user. Not the same as `/`.
