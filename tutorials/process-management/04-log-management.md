---
title: 4. Log Management
date: 2026-01-20
order: 4
---
# Log Management

Logs are essential for troubleshooting, security auditing, and system monitoring. Understanding how to find, read, and manage logs is a critical sysadmin skill.

## Log Locations

### Traditional Log Locations

| Path | Contents |
|------|----------|
| `/var/log/syslog` | General system messages (Debian/Ubuntu) |
| `/var/log/messages` | General system messages (RHEL/CentOS) |
| `/var/log/auth.log` | Authentication logs (Debian/Ubuntu) |
| `/var/log/secure` | Authentication logs (RHEL/CentOS) |
| `/var/log/dmesg` | Kernel ring buffer |
| `/var/log/kern.log` | Kernel messages |
| `/var/log/cron` | Cron job logs |
| `/var/log/maillog` | Mail server logs |
| `/var/log/boot.log` | Boot messages |
| `/var/log/faillog` | Failed login attempts |
| `/var/log/lastlog` | Last login info |

### Application Logs

| Path | Contents |
|------|----------|
| `/var/log/apache2/` | Apache web server |
| `/var/log/nginx/` | Nginx web server |
| `/var/log/mysql/` | MySQL database |
| `/var/log/postgresql/` | PostgreSQL database |

## Journald (systemd)

Modern Linux uses **journald** for centralized logging alongside traditional syslog.

### Basic journalctl Usage

```bash
# All logs
$ journalctl

# Follow new logs (like tail -f)
$ journalctl -f

# Last 100 lines
$ journalctl -n 100

# No pager (output to stdout)
$ journalctl --no-pager

# Reverse order (newest first)
$ journalctl -r
```

### Filtering by Unit

```bash
# Specific service
$ journalctl -u nginx
$ journalctl -u sshd

# Multiple services
$ journalctl -u nginx -u mysql

# Follow specific service
$ journalctl -fu nginx
```

### Filtering by Time

```bash
# Since specific time
$ journalctl --since "2024-01-15 10:00"
$ journalctl --since "1 hour ago"
$ journalctl --since yesterday
$ journalctl --since today

# Until specific time
$ journalctl --until "2024-01-15 12:00"
$ journalctl --until "30 minutes ago"

# Time range
$ journalctl --since "2024-01-15 10:00" --until "2024-01-15 12:00"
```

### Filtering by Priority

| Priority | Level | Description |
|----------|-------|-------------|
| 0 | emerg | System unusable |
| 1 | alert | Action required immediately |
| 2 | crit | Critical conditions |
| 3 | err | Error conditions |
| 4 | warning | Warning conditions |
| 5 | notice | Normal but significant |
| 6 | info | Informational |
| 7 | debug | Debug messages |

```bash
# Only errors and above
$ journalctl -p err

# Warnings from specific service
$ journalctl -p warning -u nginx

# Priority range
$ journalctl -p err..crit
```

### Filtering by Boot

```bash
# Current boot only
$ journalctl -b

# Previous boot
$ journalctl -b -1

# List all boots
$ journalctl --list-boots
```

### Other Filters

```bash
# By PID
$ journalctl _PID=1234

# By user
$ journalctl _UID=1000

# By executable
$ journalctl /usr/bin/nginx

# Kernel messages
$ journalctl -k
$ journalctl --dmesg
```

### Output Formats

```bash
# JSON output
$ journalctl -o json
$ journalctl -o json-pretty

# Verbose (all fields)
$ journalctl -o verbose

# Short with precise timestamps
$ journalctl -o short-precise

# Export format (for backup)
$ journalctl -o export > journal-backup.export
```

## Traditional Log Reading

### Using `tail`

```bash
# Last 10 lines
$ tail /var/log/syslog

# Last 50 lines
$ tail -n 50 /var/log/syslog

# Follow new entries (live)
$ tail -f /var/log/syslog

# Follow multiple files
$ tail -f /var/log/syslog /var/log/auth.log
```

### Using `less`

```bash
$ less /var/log/syslog

# Navigation:
# G     - Go to end
# g     - Go to beginning
# /text - Search forward
# ?text - Search backward
# n     - Next match
# N     - Previous match
# q     - Quit
```

### Using `grep`

```bash
# Search for pattern
$ grep "error" /var/log/syslog

# Case insensitive
$ grep -i "error" /var/log/syslog

# Show context (lines before/after)
$ grep -B 2 -A 2 "error" /var/log/syslog

# Count matches
$ grep -c "error" /var/log/syslog

# Multiple patterns
$ grep -E "error|fail|critical" /var/log/syslog
```

### Using `zgrep` for Rotated Logs

```bash
# Search compressed logs
$ zgrep "error" /var/log/syslog.2.gz

# Search all rotated logs
$ zgrep "error" /var/log/syslog*
```

## Log Rotation

Logs can grow very large. **logrotate** manages automatic rotation, compression, and deletion.

### Logrotate Configuration

Main config: `/etc/logrotate.conf`
App configs: `/etc/logrotate.d/`

```bash
$ cat /etc/logrotate.d/nginx
/var/log/nginx/*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

### Logrotate Options

| Option | Description |
|--------|-------------|
| `daily/weekly/monthly` | Rotation frequency |
| `rotate N` | Keep N rotated files |
| `compress` | Compress rotated logs |
| `delaycompress` | Compress on next rotation |
| `missingok` | Don't error if log missing |
| `notifempty` | Don't rotate if empty |
| `create` | Create new log with permissions |
| `postrotate/endscript` | Run command after rotation |

### Manual Rotation

```bash
# Force rotation
$ sudo logrotate -f /etc/logrotate.conf

# Debug (dry run)
$ sudo logrotate -d /etc/logrotate.conf

# Verbose
$ sudo logrotate -v /etc/logrotate.conf
```

## Managing Journal Size

```bash
# Check journal disk usage
$ journalctl --disk-usage
Archived and active journals take up 1.5G in the file system.

# Rotate journals
$ sudo journalctl --rotate

# Vacuum by time
$ sudo journalctl --vacuum-time=7d      # Delete > 7 days

# Vacuum by size
$ sudo journalctl --vacuum-size=500M    # Keep only 500M
```

### Permanent Journal Settings

Edit `/etc/systemd/journald.conf`:
```ini
[Journal]
SystemMaxUse=500M
SystemMaxFileSize=50M
MaxRetentionSec=1week
```

Restart journald:
```bash
$ sudo systemctl restart systemd-journald
```

## Log Analysis Tools

### `awk` for Log Parsing

```bash
# Extract specific columns
$ awk '{print $1, $4}' /var/log/nginx/access.log

# Count requests per IP
$ awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -rn | head

# Filter by status code
$ awk '$9 == 404' /var/log/nginx/access.log
```

### `last` and `lastb`

```bash
# Recent logins
$ last

# Failed logins
$ sudo lastb

# Last 10 logins
$ last -n 10

# Logins for specific user
$ last alice
```

### `dmesg` - Kernel Messages

```bash
# All kernel messages
$ dmesg

# Human-readable timestamps
$ dmesg -T

# Follow new messages
$ dmesg -w

# Filter by level
$ dmesg -l err,warn
```

## Centralized Logging

For multiple servers, use centralized logging:

| Solution | Description |
|----------|-------------|
| **rsyslog** | Forward logs to central server |
| **Elasticsearch + Kibana** | Search and visualize logs |
| **Graylog** | Open-source log management |
| **Splunk** | Enterprise log analytics |
| **Loki + Grafana** | Cloud-native logging |

### Basic rsyslog Forwarding

On client (`/etc/rsyslog.conf`):
```
*.* @logserver.example.com:514      # UDP
*.* @@logserver.example.com:514     # TCP
```

## Hands-On Exercise

1. View system logs with journalctl:
   ```bash
   $ journalctl -n 20
   $ journalctl -p err -b
   $ journalctl -u ssh --since "1 hour ago"
   ```

2. Check authentication logs:
   ```bash
   $ sudo grep "Failed" /var/log/auth.log | tail
   # or
   $ journalctl -u ssh | grep -i fail | tail
   ```

3. Monitor logs live:
   ```bash
   $ sudo tail -f /var/log/syslog
   # or
   $ journalctl -f
   ```

4. Check journal disk usage:
   ```bash
   $ journalctl --disk-usage
   ```

5. View login history:
   ```bash
   $ last -n 10
   $ who
   ```
