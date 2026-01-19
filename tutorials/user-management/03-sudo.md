---
title: 3. Sudo (Superuser Do)
date: 2026-01-20
order: 3
---
# Sudo

The `root` user has unlimited power. It is dangerous to log in as root for daily tasks.

## Using Sudo
`sudo` allows regular users to execute commands with root privileges.
- `sudo command`: Execute a single command as root
- `sudo -i`: Open a root shell (use with caution)

## Configuring Sudo
The configuration file is `/etc/sudoers`.
**NEVER** edit this file directly with a text editor.
ALWAYS use `visudo`. It checks for syntax errors before saving.

```bash
sudo visudo
```

To give a user sudo access, it's often easiest to add them to the `sudo` (Debian/Ubuntu) or `wheel` (RHEL/CentOS) group.
