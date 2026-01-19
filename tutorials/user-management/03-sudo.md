---
title: 3. Sudo (Superuser Do)
date: 2026-01-20
order: 3
---
# Sudo (Superuser Do)

The `root` user has unlimited power over the system. Logging in directly as root is dangerous and makes auditing difficult. `sudo` provides a safer alternative.

## Why Use Sudo?

| Direct root login | Using sudo |
|-------------------|------------|
| No audit trail | Commands logged to `/var/log/auth.log` |
| Unlimited access | Granular permissions possible |
| Easy to make mistakes | Requires conscious decision per command |
| Can't track who did what | User identity tracked |

## Basic Sudo Usage

```bash
$ sudo command              # Run single command as root
$ sudo -u alice command     # Run command as another user
$ sudo -i                   # Open interactive root shell
$ sudo -s                   # Open root shell (keep current environment)
$ sudo !!                   # Run last command with sudo
$ sudo -l                   # List your sudo permissions
```

### Common Examples
```bash
$ sudo apt update                      # Update package lists
$ sudo systemctl restart nginx         # Restart a service
$ sudo vim /etc/hosts                  # Edit system file
$ sudo -u postgres psql                # Run command as postgres user
```

## Sudo vs Su

| Command | Description |
|---------|-------------|
| `sudo command` | Run single command as root |
| `sudo -i` | Interactive root shell (full login) |
| `sudo -s` | Root shell (preserves environment) |
| `su -` | Switch to root (requires root password) |
| `su - alice` | Switch to alice (requires alice's password) |
| `sudo su -` | Switch to root using YOUR password |

**Key difference**: `sudo` uses YOUR password; `su` uses the TARGET user's password.

## The Sudoers File

Sudo permissions are configured in `/etc/sudoers`.

> **WARNING**: Never edit `/etc/sudoers` directly! Always use `visudo`, which validates syntax before saving. A broken sudoers file can lock you out of the system.

```bash
$ sudo visudo               # Edit sudoers file safely
$ sudo visudo -f /etc/sudoers.d/myfile   # Edit include file
```

### Sudoers File Syntax

```
who    where=(as_whom)    what
```

| Field | Description |
|-------|-------------|
| `who` | User or group (%groupname) |
| `where` | Host (usually `ALL`) |
| `as_whom` | User to run as (usually `ALL` = root) |
| `what` | Commands allowed (or `ALL`) |

### Examples

```sudoers
# Full root access
alice   ALL=(ALL:ALL) ALL

# Allow group 'sudo' full access
%sudo   ALL=(ALL:ALL) ALL

# Allow wheel group (RHEL/CentOS)
%wheel  ALL=(ALL:ALL) ALL

# Allow specific command only
bob     ALL=(ALL) /usr/bin/systemctl restart nginx

# Multiple specific commands
carol   ALL=(ALL) /usr/bin/apt update, /usr/bin/apt upgrade

# Allow without password
dave    ALL=(ALL) NOPASSWD: ALL

# Allow specific command without password
eve     ALL=(ALL) NOPASSWD: /usr/bin/docker

# Run as specific user only
deploy  ALL=(www-data) /usr/bin/git pull
```

### Using Aliases

```sudoers
# User aliases
User_Alias ADMINS = alice, bob
User_Alias WEBDEVS = carol, dave

# Command aliases
Cmnd_Alias SERVICES = /usr/bin/systemctl start *, /usr/bin/systemctl stop *, /usr/bin/systemctl restart *
Cmnd_Alias PACKAGE_MGMT = /usr/bin/apt, /usr/bin/apt-get

# Apply aliases
ADMINS  ALL=(ALL) ALL
WEBDEVS ALL=(ALL) SERVICES
```

## Adding Users to Sudo Group

The simplest way to grant sudo access:

### Debian/Ubuntu
```bash
$ sudo usermod -aG sudo username
```

### RHEL/CentOS/Fedora
```bash
$ sudo usermod -aG wheel username
```

## Drop-in Configuration

Instead of editing the main sudoers file, create files in `/etc/sudoers.d/`:

```bash
$ sudo visudo -f /etc/sudoers.d/webadmins
```

```sudoers
# /etc/sudoers.d/webadmins
%webadmins ALL=(ALL) /usr/bin/systemctl * nginx, /usr/bin/nginx -t
```

**Rules:**
- Filename must not contain `.` or `~`
- Must have correct permissions: `0440`
- Include is configured in main sudoers: `@includedir /etc/sudoers.d`

## Sudo Timeout and Options

### Timeout
By default, sudo remembers your password for 15 minutes:

```bash
$ sudo -k                   # Forget cached credentials
$ sudo -v                   # Extend timeout without running command
```

### Configure timeout in sudoers
```sudoers
Defaults        timestamp_timeout=5     # 5 minutes
Defaults        timestamp_timeout=0     # Always ask
Defaults        timestamp_timeout=-1    # Never ask again
```

### Other useful defaults
```sudoers
Defaults        logfile="/var/log/sudo.log"
Defaults        log_input, log_output
Defaults        requiretty              # Require terminal
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
```

## Sudo Security Best Practices

1. **Never give NOPASSWD: ALL** unless absolutely necessary
   ```sudoers
   # Bad
   alice ALL=(ALL) NOPASSWD: ALL
   
   # Better
   alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart myapp
   ```

2. **Use the principle of least privilege**
   - Grant only the specific commands needed
   - Use command aliases to group related commands

3. **Audit sudo usage**
   ```bash
   $ sudo grep COMMAND /var/log/auth.log
   $ sudo journalctl _COMM=sudo
   ```

4. **Use groups instead of individual users**
   ```sudoers
   %webadmins ALL=(ALL) /usr/bin/nginx
   ```

5. **Avoid shell escapes**
   ```sudoers
   # Dangerous - allows shell escape
   alice ALL=(ALL) /usr/bin/vim
   
   # Safer - use dedicated editing tool
   alice ALL=(ALL) sudoedit /etc/app/config.yml
   ```

6. **Use `sudoedit` for file editing**
   ```bash
   $ SUDO_EDITOR=vim sudoedit /etc/nginx/nginx.conf
   ```

## Troubleshooting

### User not in sudoers
```
alice is not in the sudoers file. This incident will be reported.
```
Fix: Add user to sudo group or configure in sudoers.

### Syntax error in sudoers
If you break sudoers with a manual edit:
1. Reboot to recovery mode
2. Mount root filesystem read-write: `mount -o remount,rw /`
3. Fix `/etc/sudoers`

### Test sudoers syntax
```bash
$ sudo visudo -c              # Check main file
$ sudo visudo -cf /etc/sudoers.d/myfile   # Check specific file
```

## Hands-On Exercise

1. Check your current sudo permissions:
   ```bash
   $ sudo -l
   ```

2. View sudo history:
   ```bash
   $ sudo grep sudo /var/log/auth.log | tail -10
   ```

3. Create a drop-in sudoers file:
   ```bash
   $ sudo visudo -f /etc/sudoers.d/test
   # Add: Defaults        timestamp_timeout=1
   $ sudo visudo -cf /etc/sudoers.d/test
   ```

4. Test the timeout:
   ```bash
   $ sudo ls
   # Wait 2 minutes
   $ sudo ls    # Should prompt again
   ```

5. Clean up:
   ```bash
   $ sudo rm /etc/sudoers.d/test
   ```
