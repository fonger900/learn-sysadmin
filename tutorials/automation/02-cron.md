---
title: 2. Cron Jobs
date: 2026-01-20
order: 2
---
# Cron Jobs

Cron is the standard scheduler for running commands automatically at specified times. It's essential for automation, maintenance tasks, and backups.

## How Cron Works

The cron daemon (`crond` or `cron`) runs in the background and checks every minute for scheduled tasks.

```
┌─────────── minute (0-59)
│ ┌───────── hour (0-23)
│ │ ┌─────── day of month (1-31)
│ │ │ ┌───── month (1-12)
│ │ │ │ ┌─── day of week (0-7, 0 and 7 = Sunday)
│ │ │ │ │
* * * * * command
```

## Managing Crontab

### User Crontab Commands

| Command | Description |
|---------|-------------|
| `crontab -e` | Edit your crontab |
| `crontab -l` | List your cron jobs |
| `crontab -r` | Remove your crontab |
| `crontab -u user -e` | Edit user's crontab (root) |

```bash
$ crontab -e          # Opens editor
$ crontab -l          # View current jobs
```

### Crontab Syntax

```
MIN HOUR DOM MON DOW command
```

| Field | Values | Special |
|-------|--------|---------|
| MIN | 0-59 | `-` range, `,` list, `*/n` step |
| HOUR | 0-23 | |
| DOM | 1-31 | |
| MON | 1-12 or jan-dec | |
| DOW | 0-7 or sun-sat | 0 and 7 = Sunday |

### Special Characters

| Character | Meaning | Example |
|-----------|---------|---------|
| `*` | Any value | `* * * * *` = every minute |
| `,` | List | `1,15,30` = at 1, 15, and 30 |
| `-` | Range | `1-5` = 1 through 5 |
| `/` | Step | `*/15` = every 15 |

## Common Examples

| Schedule | Cron Expression |
|----------|-----------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Every day at midnight | `0 0 * * *` |
| Every day at 3:30 AM | `30 3 * * *` |
| Every Monday at 9 AM | `0 9 * * 1` |
| First of month at noon | `0 12 1 * *` |
| Every weekday at 6 PM | `0 18 * * 1-5` |
| Twice daily (8 AM, 8 PM) | `0 8,20 * * *` |

### More Examples

```bash
# Backup every night at 2:30 AM
30 2 * * * /home/user/backup.sh

# Clear temp files every Sunday at 4 AM
0 4 * * 0 rm -rf /tmp/*

# Check disk space every hour
0 * * * * /usr/local/bin/check-disk.sh

# Run at boot (if supported)
@reboot /home/user/startup.sh
```

## Special Strings

Some cron implementations support special strings:

| String | Equivalent |
|--------|------------|
| `@reboot` | Run once at startup |
| `@yearly` | `0 0 1 1 *` |
| `@annually` | Same as @yearly |
| `@monthly` | `0 0 1 * *` |
| `@weekly` | `0 0 * * 0` |
| `@daily` | `0 0 * * *` |
| `@hourly` | `0 * * * *` |

```bash
@daily /home/user/daily-backup.sh
@reboot /home/user/start-services.sh
```

## Environment Variables

Cron runs in a minimal environment. Set variables at the top:

```bash
# Edit crontab
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin
MAILTO=admin@example.com
HOME=/home/user

# Jobs
0 * * * * /home/user/script.sh
```

### Important: PATH

Cron's PATH is minimal. Either:
1. Set PATH in crontab
2. Use absolute paths in commands

```bash
# Bad - might not find command
0 * * * * backup.sh

# Good - absolute path
0 * * * * /home/user/scripts/backup.sh

# Good - set PATH
PATH=/usr/local/bin:/usr/bin:/bin
0 * * * * backup.sh
```

## System Cron

### Cron Directories

System-wide scheduled tasks use directories:

| Directory | Runs |
|-----------|------|
| `/etc/cron.d/` | Custom cron files |
| `/etc/cron.hourly/` | Every hour |
| `/etc/cron.daily/` | Every day |
| `/etc/cron.weekly/` | Every week |
| `/etc/cron.monthly/` | Every month |

Just drop executable scripts into these directories:

```bash
# Create daily cleanup script
$ sudo vim /etc/cron.daily/cleanup
#!/bin/bash
find /tmp -mtime +7 -delete

$ sudo chmod +x /etc/cron.daily/cleanup
```

### System Crontab `/etc/crontab`

System crontab includes a user field:

```bash
# /etc/crontab
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
25 6    * * *   root    test -x /usr/sbin/anacron || run-parts --report /etc/cron.daily
```

### `/etc/cron.d/` Files

Custom cron files with the same syntax as `/etc/crontab`:

```bash
# /etc/cron.d/myapp
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

# Run as www-data every 10 minutes
*/10 * * * * www-data /var/www/app/cleanup.sh
```

## Output and Logging

### Email Output

By default, cron emails output to the user:

```bash
# Send output to specific email
MAILTO=admin@example.com
0 * * * * /home/user/script.sh

# Disable email
MAILTO=""
0 * * * * /home/user/script.sh
```

### Redirect Output

```bash
# Discard all output
0 * * * * /script.sh > /dev/null 2>&1

# Log to file
0 * * * * /script.sh >> /var/log/script.log 2>&1

# Log with timestamp
0 * * * * /script.sh 2>&1 | ts >> /var/log/script.log
```

### View Cron Logs

```bash
# Debian/Ubuntu
$ grep CRON /var/log/syslog

# RHEL/CentOS
$ cat /var/log/cron

# Using journalctl
$ journalctl -u cron
$ journalctl -u crond
```

## Anacron

Anacron runs jobs that were missed due to downtime—useful for laptops and desktops.

### Anacron Configuration

`/etc/anacrontab`:
```
# period  delay  job-id    command
1         5      cron.daily    run-parts /etc/cron.daily
7         10     cron.weekly   run-parts /etc/cron.weekly
@monthly  15     cron.monthly  run-parts /etc/cron.monthly
```

| Field | Description |
|-------|-------------|
| period | Days between runs |
| delay | Minutes to wait after boot |
| job-id | Unique identifier |
| command | Command to run |

Anacron tracks last run in `/var/spool/anacron/`.

## Access Control

### Allow/Deny Users

| File | Effect |
|------|--------|
| `/etc/cron.allow` | Only listed users can use cron |
| `/etc/cron.deny` | Listed users cannot use cron |

If `cron.allow` exists, only users in it can use cron.
If only `cron.deny` exists, everyone except listed users can use cron.

## Debugging Cron Jobs

### Common Issues

1. **PATH not set**
   ```bash
   # Fix: Use absolute paths or set PATH
   PATH=/usr/local/bin:/usr/bin:/bin
   ```

2. **Environment variables missing**
   ```bash
   # Fix: Set variables or use a wrapper script
   0 * * * * . /home/user/.profile; /script.sh
   ```

3. **Permissions**
   ```bash
   # Fix: Make script executable
   $ chmod +x /home/user/script.sh
   ```

4. **Not using /bin/bash**
   ```bash
   # Fix: Set shell
   SHELL=/bin/bash
   ```

### Test Your Cron Job

```bash
# Run as cron would
$ env -i /bin/bash -c '/path/to/script.sh'

# Or check minimal environment
$ env -i SHELL=/bin/sh PATH=/usr/bin:/bin /path/to/script.sh
```

## Cron vs Systemd Timers

Modern alternative using systemd:

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Daily backup timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Backup service

[Service]
Type=oneshot
ExecStart=/home/user/backup.sh
```

```bash
$ sudo systemctl enable --now backup.timer
$ systemctl list-timers
```

## Hands-On Exercise

1. View existing cron jobs:
   ```bash
   $ crontab -l
   $ ls -la /etc/cron.*
   $ cat /etc/crontab
   ```

2. Create a simple cron job:
   ```bash
   $ crontab -e
   # Add: */5 * * * * echo "$(date)" >> /tmp/cron-test.log
   # Wait 5 minutes, then check:
   $ cat /tmp/cron-test.log
   ```

3. Check cron logs:
   ```bash
   $ grep CRON /var/log/syslog | tail
   # or
   $ journalctl -u cron --since "1 hour ago"
   ```

4. Create a system cron script:
   ```bash
   $ sudo vim /etc/cron.daily/test-cleanup
   #!/bin/bash
   echo "Cleanup ran at $(date)" >> /tmp/cleanup.log
   $ sudo chmod +x /etc/cron.daily/test-cleanup
   ```

5. Clean up:
   ```bash
   $ crontab -e   # Remove the test job
   $ rm /tmp/cron-test.log
   $ sudo rm /etc/cron.daily/test-cleanup
   ```
