---
title: 3. Swap Space
date: 2026-01-20
order: 3
---
# Swap Space

Swap space extends your system's memory by using disk space. When RAM is full, the kernel moves less-used memory pages to swap, freeing RAM for active processes.

## What is Swap?

| RAM | Swap | Effect |
|-----|------|--------|
| Sufficient | None | System works normally |
| Full | Available | System uses swap, slows down |
| Full | Full | OOM killer terminates processes |

### Types of Swap

| Type | Description | Flexibility |
|------|-------------|-------------|
| **Swap Partition** | Dedicated disk partition | Less flexible |
| **Swap File** | Regular file used as swap | More flexible |

**Modern recommendation**: Use swap files for flexibility.

## Viewing Current Swap

```bash
# View swap usage
$ free -h
              total        used        free      shared  buff/cache   available
Mem:          7.8Gi       4.2Gi       1.1Gi       156Mi       2.4Gi       3.2Gi
Swap:         2.0Gi          0B       2.0Gi

# Detailed swap info
$ swapon --show
NAME      TYPE      SIZE   USED PRIO
/swapfile file        2G     0B   -2

# From /proc
$ cat /proc/swaps
```

## Creating a Swap File

### Step 1: Create the File

```bash
# Create a 2GB swap file
$ sudo fallocate -l 2G /swapfile

# Alternative (if fallocate not supported)
$ sudo dd if=/dev/zero of=/swapfile bs=1M count=2048

# Verify
$ ls -lh /swapfile
```

### Step 2: Set Permissions

```bash
# Only root should access swap
$ sudo chmod 600 /swapfile
```

### Step 3: Set Up Swap Area

```bash
$ sudo mkswap /swapfile
Setting up swapspace version 1, size = 2 GiB (2147479552 bytes)
```

### Step 4: Enable Swap

```bash
$ sudo swapon /swapfile

# Verify
$ swapon --show
$ free -h
```

### Step 5: Make Permanent

Add to `/etc/fstab`:
```bash
$ echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

Or manually edit `/etc/fstab`:
```
/swapfile    none    swap    sw    0    0
```

## Creating a Swap Partition

### Step 1: Create Partition

```bash
$ sudo fdisk /dev/sdb

Command: n          # New partition
Command: t          # Change type
Hex code: 82        # Linux swap
Command: w          # Write
```

### Step 2: Set Up and Enable

```bash
$ sudo mkswap /dev/sdb1
$ sudo swapon /dev/sdb1
```

### Step 3: Make Permanent

Add to `/etc/fstab`:
```
/dev/sdb1    none    swap    sw    0    0

# Or use UUID (recommended)
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx    none    swap    sw    0    0
```

Get UUID:
```bash
$ sudo blkid /dev/sdb1
```

## Managing Swap

### Enable/Disable Swap

```bash
# Enable specific swap
$ sudo swapon /swapfile
$ sudo swapon /dev/sdb1

# Enable all swap in fstab
$ sudo swapon -a

# Disable specific swap
$ sudo swapoff /swapfile
$ sudo swapoff /dev/sdb1

# Disable all swap
$ sudo swapoff -a
```

### Checking Swap Usage

```bash
$ free -h
$ swapon --show
$ vmstat 1 5          # si/so columns show swap in/out
```

## Swap Priority

When multiple swap spaces exist, priority determines which is used first:

```bash
# Higher number = higher priority
$ sudo swapon -p 10 /swapfile
$ sudo swapon -p 5 /dev/sdb1

# In fstab
/swapfile    none    swap    sw,pri=10    0    0
/dev/sdb1    none    swap    sw,pri=5     0    0
```

## Resizing Swap

### Increase Swap File

```bash
# Disable current swap
$ sudo swapoff /swapfile

# Resize file
$ sudo fallocate -l 4G /swapfile
# or
$ sudo dd if=/dev/zero of=/swapfile bs=1M count=4096

# Reinitialize
$ sudo mkswap /swapfile

# Re-enable
$ sudo swapon /swapfile
```

### Decrease Swap File

```bash
# First, disable
$ sudo swapoff /swapfile

# Then resize and reinitialize
$ sudo fallocate -l 1G /swapfile
$ sudo chmod 600 /swapfile
$ sudo mkswap /swapfile
$ sudo swapon /swapfile
```

## Swappiness

Swappiness controls how aggressively the kernel uses swap (0-100):

| Value | Behavior |
|-------|----------|
| 0 | Avoid swap unless absolutely necessary |
| 10 | Minimal swapping (recommended for SSDs) |
| 60 | Default on most systems |
| 100 | Swap aggressively |

### Check Current Value

```bash
$ cat /proc/sys/vm/swappiness
60
```

### Set Temporarily

```bash
$ sudo sysctl vm.swappiness=10
```

### Set Permanently

Add to `/etc/sysctl.conf` or create `/etc/sysctl.d/99-swappiness.conf`:
```bash
$ echo 'vm.swappiness=10' | sudo tee /etc/sysctl.d/99-swappiness.conf
$ sudo sysctl -p /etc/sysctl.d/99-swappiness.conf
```

## How Much Swap Do You Need?

General recommendations:

| RAM | Swap (No Hibernation) | Swap (With Hibernation) |
|-----|----------------------|-------------------------|
| ≤ 2 GB | 2x RAM | 3x RAM |
| 2-8 GB | Equal to RAM | 2x RAM |
| 8-64 GB | At least 4 GB | 1.5x RAM |
| > 64 GB | At least 4 GB | Not practical |

**For servers**: Start with 1-2 GB and monitor usage.

## Monitoring Swap Usage

### Using `vmstat`

```bash
$ vmstat 1 5
procs -----------memory---------- ---swap-- -----io----
 r  b   swpd   free   buff  cache   si   so    bi    bo
 1  0      0 1234567  12345 567890    0    0     5     3
```

| Column | Meaning |
|--------|---------|
| `swpd` | Virtual memory used (KB) |
| `si` | Swap in (KB/s) |
| `so` | Swap out (KB/s) |

### Using `sar`

```bash
$ sar -S 1 5           # Swap statistics
$ sar -W 1 5           # Swap pages/sec
```

## Clearing Swap

To clear swap (moves data back to RAM):

```bash
# Check you have enough free RAM first!
$ free -h

# Clear swap
$ sudo swapoff -a && sudo swapon -a
```

## Hands-On Exercise

1. Check current swap:
   ```bash
   $ free -h
   $ swapon --show
   $ cat /proc/swaps
   ```

2. Check swappiness:
   ```bash
   $ cat /proc/sys/vm/swappiness
   ```

3. Create a small test swap file (50MB):
   ```bash
   $ sudo dd if=/dev/zero of=/tmp/testswap bs=1M count=50
   $ sudo chmod 600 /tmp/testswap
   $ sudo mkswap /tmp/testswap
   $ sudo swapon /tmp/testswap
   $ swapon --show
   ```

4. Clean up:
   ```bash
   $ sudo swapoff /tmp/testswap
   $ sudo rm /tmp/testswap
   $ swapon --show
   ```
