---
title: 2. Mounting
date: 2026-01-20
order: 2
---
# Mounting

Accessing a filesystem by attaching it to the directory tree.

## Mounting
- `mount /dev/sda1 /mnt`: Attach partition to `/mnt`
- `umount /mnt`: Detach

## Permanent Mounting (`/etc/fstab`)
To mount automatically at boot, add an entry to `/etc/fstab`.
Format:
`UUID=xxxx /mountpoint ext4 defaults 0 0`

Use `blkid` to find the UUID of a partition.
**WARNING**: Errors in fstab can prevent boot.
