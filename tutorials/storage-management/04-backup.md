---
title: 4. Backup and Restore
date: 2026-01-20
order: 4
---
# Backup and Restore

Backups are your safety net. A solid backup strategy protects against hardware failure, human error, ransomware, and disasters.

## The 3-2-1 Backup Rule

| Number | Meaning |
|--------|---------|
| **3** | Keep 3 copies of data |
| **2** | On 2 different storage types |
| **1** | With 1 copy offsite |

Example:
- Original on server SSD
- Backup on local NAS
- Offsite backup in cloud

## tar - Tape Archive

The classic Unix backup tool. Creates compressed archives.

### Creating Archives

```bash
# Create archive
$ tar -cvf backup.tar /path/to/files

# Create compressed archive (gzip)
$ tar -czvf backup.tar.gz /path/to/files

# Create compressed archive (bzip2 - smaller but slower)
$ tar -cjvf backup.tar.bz2 /path/to/files

# Create compressed archive (xz - smallest but slowest)
$ tar -cJvf backup.tar.xz /path/to/files
```

| Flag | Meaning |
|------|---------|
| `-c` | Create archive |
| `-v` | Verbose |
| `-f` | Filename |
| `-z` | gzip compression |
| `-j` | bzip2 compression |
| `-J` | xz compression |
| `-p` | Preserve permissions |

### Viewing Contents

```bash
$ tar -tvf backup.tar.gz        # List contents
$ tar -tzvf backup.tar.gz       # With compression details
```

### Extracting Archives

```bash
# Extract to current directory
$ tar -xzvf backup.tar.gz

# Extract to specific directory
$ tar -xzvf backup.tar.gz -C /path/to/destination

# Extract specific files
$ tar -xzvf backup.tar.gz path/to/specific/file
```

### Practical Examples

```bash
# Backup home directory
$ tar -czvf home-backup-$(date +%Y%m%d).tar.gz /home/

# Backup with exclusions
$ tar -czvf backup.tar.gz --exclude='*.log' --exclude='cache/' /var/www/

# Backup preserving permissions
$ tar -cpzvf backup.tar.gz /etc/

# Incremental backup (files newer than date)
$ tar -czvf incremental.tar.gz --newer="2024-01-15" /data/
```

## rsync - Remote Sync

The most versatile backup tool. Copies only changed files.

### Basic Syntax

```bash
rsync [options] source destination
```

### Common Options

| Option | Description |
|--------|-------------|
| `-a` | Archive mode (preserves everything) |
| `-v` | Verbose |
| `-z` | Compress during transfer |
| `-h` | Human-readable output |
| `-P` | Show progress + resume |
| `--delete` | Delete files not in source |
| `-n` | Dry run |
| `-e ssh` | Use SSH |

### Local Backups

```bash
# Basic sync
$ rsync -av /source/ /destination/

# With progress
$ rsync -avhP /source/ /destination/

# Mirror (delete extra files in destination)
$ rsync -av --delete /source/ /destination/

# Dry run (test first!)
$ rsync -avn --delete /source/ /destination/
```

> **Note**: Trailing slash matters!
> - `/source/` copies contents
> - `/source` copies the directory itself

### Remote Backups

```bash
# Push to remote
$ rsync -avzP /local/path/ user@server:/remote/path/

# Pull from remote
$ rsync -avzP user@server:/remote/path/ /local/path/

# With specific SSH port
$ rsync -avzP -e "ssh -p 2222" /local/ user@server:/remote/

# With bandwidth limit (KB/s)
$ rsync -avz --bwlimit=5000 /source/ user@server:/destination/
```

### Exclude Patterns

```bash
# Exclude patterns
$ rsync -av --exclude='*.log' --exclude='cache/' /source/ /dest/

# Exclude from file
$ rsync -av --exclude-from='exclude.txt' /source/ /dest/
```

`exclude.txt`:
```
*.log
*.tmp
cache/
.git/
node_modules/
```

### rsync Backup Script

```bash
#!/bin/bash
# backup.sh

SOURCE="/var/www/"
DESTINATION="/backup/www/"
LOG="/var/log/backup.log"

echo "$(date): Starting backup" >> $LOG

rsync -av --delete \
    --exclude='*.log' \
    --exclude='cache/' \
    "$SOURCE" "$DESTINATION" \
    >> $LOG 2>&1

echo "$(date): Backup complete" >> $LOG
```

## Backup Strategies

### Full Backup

Complete copy of all data.
- **Pros**: Simple restore
- **Cons**: Time and space consuming

### Incremental Backup

Only files changed since last backup.
- **Pros**: Fast, small
- **Cons**: Restore requires all incrementals

### Differential Backup

Files changed since last full backup.
- **Pros**: Faster restore than incremental
- **Cons**: Grows larger over time

### Snapshot

Point-in-time copy (filesystem level).
- **Pros**: Instant, minimal space
- **Cons**: Same disk (not offsite)

## Database Backups

### MySQL/MariaDB

```bash
# Dump single database
$ mysqldump -u root -p database_name > backup.sql

# Dump all databases
$ mysqldump -u root -p --all-databases > all-databases.sql

# Dump with compression
$ mysqldump -u root -p database_name | gzip > backup.sql.gz

# Restore
$ mysql -u root -p database_name < backup.sql
$ zcat backup.sql.gz | mysql -u root -p database_name
```

### PostgreSQL

```bash
# Dump database
$ pg_dump database_name > backup.sql

# Dump all databases
$ pg_dumpall > all-databases.sql

# Custom format (compressed, flexible restore)
$ pg_dump -Fc database_name > backup.dump

# Restore
$ psql database_name < backup.sql
$ pg_restore -d database_name backup.dump
```

## Rotation and Retention

### Simple Date-Based Script

```bash
#!/bin/bash
BACKUP_DIR="/backup"
DAYS_TO_KEEP=7

# Create backup
tar -czvf "$BACKUP_DIR/backup-$(date +%Y%m%d).tar.gz" /data/

# Delete old backups
find "$BACKUP_DIR" -name "backup-*.tar.gz" -mtime +$DAYS_TO_KEEP -delete
```

### Grandfather-Father-Son (GFS)

| Level | Frequency | Retention |
|-------|-----------|-----------|
| Daily | Every day | 7 days |
| Weekly | Every Sunday | 4 weeks |
| Monthly | 1st of month | 12 months |

## Verification

**Always test your backups!**

```bash
# Test tar archive integrity
$ tar -tzvf backup.tar.gz > /dev/null && echo "OK"

# Test with checksum
$ md5sum backup.tar.gz > backup.tar.gz.md5
$ md5sum -c backup.tar.gz.md5

# Actually restore to test location
$ mkdir /tmp/restore-test
$ tar -xzvf backup.tar.gz -C /tmp/restore-test
$ diff -r /original/path /tmp/restore-test/path
```

## Automation with Cron

```bash
# /etc/cron.d/backup
SHELL=/bin/bash
PATH=/usr/local/bin:/usr/bin:/bin

# Daily backup at 2:30 AM
30 2 * * * root /usr/local/bin/backup.sh >> /var/log/backup.log 2>&1

# Weekly full backup on Sunday at 3 AM
0 3 * * 0 root /usr/local/bin/full-backup.sh
```

## Cloud Backup Tools

| Tool | Cloud Provider |
|------|----------------|
| `aws s3` | Amazon S3 |
| `gsutil` | Google Cloud Storage |
| `azcopy` | Azure Blob Storage |
| `rclone` | Multi-cloud (recommended) |

### rclone Example

```bash
# Configure remote
$ rclone config

# Sync to cloud
$ rclone sync /local/path remote:bucket/path

# With bandwidth limit
$ rclone sync --bwlimit 10M /local/path remote:bucket/path
```

## Disaster Recovery Plan

1. **Document everything**
   - What to backup
   - Where backups are stored
   - How to restore

2. **Test regularly**
   - Monthly: Verify backup integrity
   - Quarterly: Full restore test

3. **Monitor backups**
   - Check if backups ran
   - Alert on failures
   - Verify backup size

## Hands-On Exercise

1. Create a tar backup:
   ```bash
   $ tar -czvf ~/backup-test.tar.gz /etc/hostname /etc/hosts
   $ tar -tzvf ~/backup-test.tar.gz
   ```

2. Practice rsync:
   ```bash
   $ mkdir ~/source ~/dest
   $ touch ~/source/file{1..5}.txt
   $ rsync -avh ~/source/ ~/dest/
   $ ls ~/dest/
   ```

3. Test incremental rsync:
   ```bash
   $ touch ~/source/file6.txt
   $ rsync -avh ~/source/ ~/dest/
   # Notice only file6.txt is transferred
   ```

4. Clean up:
   ```bash
   $ rm -rf ~/backup-test.tar.gz ~/source ~/dest
   ```
