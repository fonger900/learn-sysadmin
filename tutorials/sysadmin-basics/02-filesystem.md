---
title: 2. Filesystem Hierarchy
date: 2026-01-20
order: 2
---
# Linux Filesystem Hierarchy

In Linux, everything is organized as a file—including hardware devices, processes, and configuration. Understanding the filesystem hierarchy is essential for navigating and managing a Linux system.

## The Root of Everything

The filesystem starts at `/` (root directory), not to be confused with `/root` (the root user's home directory).

```
/
├── bin/
├── boot/
├── dev/
├── etc/
├── home/
├── lib/
├── media/
├── mnt/
├── opt/
├── proc/
├── root/
├── run/
├── sbin/
├── srv/
├── sys/
├── tmp/
├── usr/
└── var/
```

## Filesystem Hierarchy Standard (FHS)

The FHS defines the directory structure for Unix-like systems:

| Directory | Purpose | Examples |
|-----------|---------|----------|
| `/` | Root directory, top of the hierarchy | — |
| `/bin` | Essential user command binaries | `ls`, `cp`, `cat`, `bash` |
| `/sbin` | Essential system binaries (admin) | `fdisk`, `ifconfig`, `reboot` |
| `/boot` | Boot loader files, kernel | `vmlinuz`, `initrd`, `grub/` |
| `/dev` | Device files | `/dev/sda`, `/dev/null`, `/dev/tty` |
| `/etc` | System-wide configuration files | `passwd`, `fstab`, `ssh/` |
| `/home` | User home directories | `/home/alice`, `/home/bob` |
| `/lib` | Shared libraries for `/bin` and `/sbin` | `.so` files |
| `/media` | Mount point for removable media | USB drives, CD-ROMs |
| `/mnt` | Temporary mount point | Manual mounts |
| `/opt` | Optional/add-on software packages | Third-party apps |
| `/proc` | Virtual filesystem for process info | `/proc/cpuinfo`, `/proc/meminfo` |
| `/root` | Root user's home directory | Config files for root |
| `/run` | Runtime variable data | PID files, sockets |
| `/srv` | Data for services | Web server data |
| `/sys` | Virtual filesystem for kernel/hardware | Device info |
| `/tmp` | Temporary files (cleared on reboot) | Session data |
| `/usr` | Secondary hierarchy for user data | Most programs |
| `/var` | Variable data (logs, caches, mail) | `/var/log`, `/var/cache` |

## Key Directories in Detail

### `/etc` - Configuration Central
All system-wide configuration lives here:
```bash
/etc/passwd      # User account information
/etc/shadow      # Encrypted passwords
/etc/group       # Group definitions
/etc/fstab       # Filesystem mount table
/etc/hosts       # Static hostname resolution
/etc/ssh/        # SSH server/client config
/etc/cron.d/     # Cron job definitions
/etc/systemd/    # Systemd unit files
```

### `/var` - Variable Data
Data that changes during system operation:
```bash
/var/log/        # System and application logs
/var/cache/      # Application cache
/var/spool/      # Print queues, mail queues
/var/lib/        # Persistent application data
/var/tmp/        # Temporary files preserved across reboots
```

### `/usr` - User Programs
Most user-level programs and data:
```bash
/usr/bin/        # User commands
/usr/sbin/       # System admin commands
/usr/lib/        # Libraries for /usr/bin and /usr/sbin
/usr/local/      # Locally installed software
/usr/share/      # Architecture-independent data
/usr/share/man/  # Manual pages
```

### `/proc` - Process Information
Virtual filesystem providing process and system info:
```bash
$ cat /proc/cpuinfo      # CPU information
$ cat /proc/meminfo      # Memory information
$ cat /proc/uptime       # System uptime
$ ls /proc/1234/         # Info about process PID 1234
```

## Absolute vs Relative Paths

| Type | Description | Example |
|------|-------------|---------|
| **Absolute** | Full path from root `/` | `/home/user/documents/file.txt` |
| **Relative** | Path from current directory | `./documents/file.txt` or `../parent/` |

**Special path symbols:**
- `.` — Current directory
- `..` — Parent directory
- `~` — Home directory
- `-` — Previous directory (with `cd`)

```bash
$ pwd
/home/user
$ cd ./documents       # Same as: cd documents
$ cd ../               # Go to /home
$ cd ~                 # Go to /home/user
$ cd -                 # Return to previous directory
```

## Navigating Efficiently

```bash
# Find where you are
$ pwd
/var/log

# Move around
$ cd /etc              # Absolute path
$ cd ../../home/user   # Relative path
$ cd                   # Go home (same as cd ~)
$ cd -                 # Go back to /etc

# List and explore
$ ls -la /etc          # List with details
$ tree /etc -L 2       # Tree view, 2 levels deep
```

## Hands-On Exercise

1. Navigate to the root directory and list its contents:
   ```bash
   $ cd /
   $ ls -la
   ```

2. Explore `/etc` and find configuration files:
   ```bash
   $ ls /etc/*.conf | head -10
   ```

3. Check system information from `/proc`:
   ```bash
   $ cat /proc/cpuinfo | grep "model name" | head -1
   $ cat /proc/meminfo | grep MemTotal
   ```

4. Practice relative paths:
   ```bash
   $ cd /var/log
   $ cd ../../etc
   $ pwd    # Should show /etc
   ```

5. Find where common commands live:
   ```bash
   $ which ls
   $ which python
   $ which systemctl
   ```
