---
title: 2. Cron Jobs
date: 2026-01-20
order: 2
---
# Cron Jobs

Schedule scripts to run automatically at specific times.

## Crontab
The configuration file for cron.
- `crontab -e`: Edit current user's crontab
- `crontab -l`: List jobs

## Syntax
`m h dom mon dow command`
- `m`: Minute (0-59)
- `h`: Hour (0-23)
- `dom`: Day of Month (1-31)
- `mon`: Month (1-12)
- `dow`: Day of Week (0-7, 0/7=Sunday)

## Examples
- `0 5 * * * /path/backup.sh`: Run at 5:00 AM every day
- `*/15 * * * * /path/check.sh`: Run every 15 minutes
