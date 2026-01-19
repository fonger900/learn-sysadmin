---
title: 2. Mounting Filesystems
date: 2026-01-20
order: 2
---
# Mounting Filesystems

In Linux, filesystems must be "mounted" to access them. Mounting attaches a filesystem to a directory in the file tree.

## The Mount Concept

```
┌─────────────────────────────────────────────┐
│                    /                         │
├─────────┬───────────┬───────────────────────┤
│  /home  │   /var    │        /mnt           │
│ (disk1) │  (disk1)  │        │              │
│         │           │    ┌───┴───┐          │
│         │           │    │ data  │          │
│         │           │    │(sdb1) │          │
│         │           │    │mounted│          │
└─────────┴───────────┴────┴───────┴──────────┘
```

## Basic Mount Commands

### Mounting

```bash
# Basic mount
$ sudo mount /dev/sdb1 /mnt

# Mount with filesystem type
$ sudo mount -t ext4 /dev/sdb1 /mnt

# Mount with options
$ sudo mount -o ro /dev/sdb1 /mnt      # Read-only
$ sudo mount -o rw /dev/sdb1 /mnt      # Read-write
```

### Unmounting

```bash
$ sudo umount /mnt
$ sudo umount /dev/sdb1        # By device

# Force unmount (if busy)
$ sudo umount -l /mnt          # Lazy unmount
$ sudo umount -f /mnt          # Force (NFS)

# Find what's using the mount
$ lsof +D /mnt
$ fuser -v /mnt
$ fuser -km /mnt               # Kill processes
```

### Viewing Mounts

```bash
$ mount                        # All mounts
$ mount | grep sdb             # Specific device
$ findmnt                      # Tree view
$ findmnt /mnt                 # Specific mount
$ cat /proc/mounts             # Kernel view
```

## Mount Options

### Common Options

| Option | Description |
|--------|-------------|
| `rw` | Read-write (default) |
| `ro` | Read-only |
| `noexec` | No execution of binaries |
| `nosuid` | Ignore SUID bits |
| `nodev` | Ignore device files |
| `noatime` | Don't update access time |
| `nodiratime` | Don't update dir access time |
| `sync` | Sync writes immediately |
| `async` | Async writes (default) |
| `auto` | Can be mounted with `mount -a` |
| `noauto` | Don't mount with `mount -a` |
| `user` | Allow non-root to mount |
| `users` | Allow any user to mount/unmount |
| `defaults` | rw, suid, dev, exec, auto, nouser, async |

### Security Options

```bash
# Secure mount for user data
$ sudo mount -o noexec,nosuid,nodev /dev/sdb1 /data

# Read-only mount
$ sudo mount -o ro /dev/sdb1 /data
```

## Permanent Mounts: `/etc/fstab`

The `/etc/fstab` file defines automatic mounts at boot.

### Format

```
<device>    <mount_point>    <fs_type>    <options>    <dump>    <pass>
```

| Field | Description |
|-------|-------------|
| device | Device path, UUID, or LABEL |
| mount_point | Where to mount |
| fs_type | Filesystem type |
| options | Mount options |
| dump | 0 = no backup, 1 = backup |
| pass | fsck order (0 = skip, 1 = root, 2 = others) |

### Example `/etc/fstab`

```bash
# <device>                                  <mount>    <type>  <options>        <dump> <pass>
UUID=abc123-def456                          /          ext4    defaults         0      1
UUID=789xyz-uvw012                          /home      ext4    defaults         0      2
UUID=swap-uuid-here                         none       swap    sw               0      0
/dev/sdb1                                   /data      ext4    defaults,noatime 0      2
//server/share                              /mnt/nas   cifs    credentials=/etc/cifs-cred 0 0
192.168.1.100:/export                       /mnt/nfs   nfs     defaults         0      0
```

### Getting UUIDs

```bash
$ sudo blkid
$ sudo blkid /dev/sdb1
/dev/sdb1: UUID="abc123-def456" TYPE="ext4"

# Or use lsblk
$ lsblk -o NAME,UUID,FSTYPE
```

### Testing fstab

```bash
# Test before reboot!
$ sudo mount -a                # Mount all in fstab

# Mount specific entry
$ sudo mount /data             # Just specify mount point
```

> **WARNING**: Errors in `/etc/fstab` can prevent boot! Always test with `mount -a` before rebooting.

## Bind Mounts

Bind mounts make a directory available at another location:

```bash
# Mount directory to another location
$ sudo mount --bind /var/www /home/user/website

# Make permanent in fstab
/var/www    /home/user/website    none    bind    0    0

# Read-only bind mount
$ sudo mount --bind -o ro /var/log /home/user/logs
```

**Use cases:**
- Chroot environments
- Containers
- Sharing directories between users
- Accessing directories in restricted environments

## Loop Devices

Mount disk images as filesystems:

```bash
# Mount ISO file
$ sudo mount -o loop image.iso /mnt/iso

# Mount disk image
$ sudo mount -o loop disk.img /mnt/disk

# Create and mount a file as filesystem
$ dd if=/dev/zero of=/tmp/disk.img bs=1M count=100
$ mkfs.ext4 /tmp/disk.img
$ sudo mount -o loop /tmp/disk.img /mnt
```

### Managing Loop Devices

```bash
$ losetup -l                   # List loop devices
$ sudo losetup /dev/loop0 /path/to/image   # Create
$ sudo losetup -d /dev/loop0   # Detach
```

## tmpfs - RAM-based Filesystem

tmpfs uses RAM (and swap) for temporary storage:

```bash
# Mount tmpfs
$ sudo mount -t tmpfs -o size=512M tmpfs /mnt/ramdisk

# In fstab
tmpfs    /mnt/ramdisk    tmpfs    size=512M,nodev,nosuid    0    0
```

**Common tmpfs mounts:**
- `/tmp` - Temporary files
- `/run` - Runtime data
- `/dev/shm` - Shared memory

## Systemd Mount Units

Systemd can manage mounts using `.mount` unit files:

```ini
# /etc/systemd/system/data.mount
[Unit]
Description=Data Partition

[Mount]
What=/dev/sdb1
Where=/data
Type=ext4
Options=defaults,noatime

[Install]
WantedBy=multi-user.target
```

```bash
$ sudo systemctl daemon-reload
$ sudo systemctl start data.mount
$ sudo systemctl enable data.mount
```

The filename must match the mount path: `/data` → `data.mount`

## Automount with autofs

Automatically mount on access:

```bash
$ sudo apt install autofs

# /etc/auto.master
/mnt/auto    /etc/auto.usb    --timeout=60

# /etc/auto.usb
usb    -fstype=auto    :/dev/sdb1

$ sudo systemctl restart autofs
$ ls /mnt/auto/usb       # Triggers mount
```

## Troubleshooting

### "Device is busy"

```bash
# Find what's using it
$ lsof +D /mnt
$ fuser -v /mnt

# Kill processes
$ fuser -km /mnt

# Lazy unmount
$ sudo umount -l /mnt
```

### "Wrong fs type"

```bash
$ sudo blkid /dev/sdb1           # Check actual type
$ sudo mount -t ext4 /dev/sdb1 /mnt   # Specify type
```

### Mount at boot fails

```bash
# Check fstab syntax
$ sudo mount -a

# Add 'nofail' option for non-critical mounts
UUID=xxx    /data    ext4    defaults,nofail    0    2
```

## Hands-On Exercise

1. View current mounts:
   ```bash
   $ mount | grep -E "^/dev"
   $ findmnt --fstab
   $ cat /etc/fstab
   ```

2. Get UUID of a partition:
   ```bash
   $ sudo blkid
   ```

3. Create a tmpfs mount:
   ```bash
   $ sudo mount -t tmpfs -o size=100M tmpfs /mnt
   $ df -h /mnt
   $ sudo umount /mnt
   ```

4. Practice bind mount:
   ```bash
   $ mkdir ~/bind-test
   $ sudo mount --bind /var/log ~/bind-test
   $ ls ~/bind-test
   $ sudo umount ~/bind-test
   ```

5. Create and mount a loop device:
   ```bash
   $ dd if=/dev/zero of=/tmp/test.img bs=1M count=50
   $ mkfs.ext4 /tmp/test.img
   $ sudo mount -o loop /tmp/test.img /mnt
   $ df -h /mnt
   $ sudo umount /mnt
   $ rm /tmp/test.img
   ```
