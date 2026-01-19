---
title: 1. Partitions and Filesystems
date: 2026-01-20
order: 1
---
# Partitions and Filesystems

Understanding storage is fundamental to system administration. This tutorial covers how Linux sees disks, partitioning, and filesystem creation.

## Block Devices

In Linux, storage devices are represented as block devices in `/dev/`:

| Device | Description |
|--------|-------------|
| `/dev/sda` | First SATA/SCSI disk |
| `/dev/sdb` | Second SATA/SCSI disk |
| `/dev/sda1` | First partition on sda |
| `/dev/nvme0n1` | First NVMe SSD |
| `/dev/nvme0n1p1` | First partition on NVMe |
| `/dev/vda` | Virtual disk (VMs) |
| `/dev/xvda` | Xen virtual disk (AWS) |

## Viewing Disks and Partitions

### `lsblk` - List Block Devices

```bash
$ lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0   100G  0 disk 
├─sda1   8:1    0   500M  0 part /boot
├─sda2   8:2    0    50G  0 part /
└─sda3   8:3    0  49.5G  0 part /home
sdb      8:16   0   500G  0 disk 
└─sdb1   8:17   0   500G  0 part /data
```

```bash
$ lsblk -f                    # Show filesystem types
$ lsblk -o NAME,SIZE,TYPE,MOUNTPOINT,FSTYPE,UUID
```

### `fdisk -l` - Detailed Disk Info

```bash
$ sudo fdisk -l /dev/sda
Disk /dev/sda: 100 GiB, 107374182400 bytes, 209715200 sectors
...
Device     Boot   Start       End   Sectors  Size Id Type
/dev/sda1  *       2048   1026047   1024000  500M 83 Linux
/dev/sda2       1026048  99614619  98588572   47G 83 Linux
```

### `df` - Disk Free Space

```bash
$ df -h                       # Human-readable
$ df -hT                      # Include filesystem type
$ df -h /home                 # Specific mount
```

### `du` - Disk Usage

```bash
$ du -sh /var/log             # Size of directory
$ du -h --max-depth=1 /       # One level of /
$ du -h /home | sort -rh | head   # Largest dirs
```

## Partition Tables: MBR vs GPT

| Feature | MBR | GPT |
|---------|-----|-----|
| Max disk size | 2 TB | 9.4 ZB |
| Max partitions | 4 primary (+ extended) | 128 |
| Boot mode | BIOS | UEFI |
| Redundancy | None | Backup header |
| Age | Legacy | Modern |

**Recommendation:** Use GPT for new systems.

## Partitioning with `fdisk` (MBR/GPT)

`fdisk` is an interactive partitioning tool:

```bash
$ sudo fdisk /dev/sdb
```

### Common `fdisk` Commands

| Command | Description |
|---------|-------------|
| `p` | Print partition table |
| `n` | Create new partition |
| `d` | Delete partition |
| `t` | Change partition type |
| `w` | Write changes and exit |
| `q` | Quit without saving |
| `g` | Create new GPT table |
| `o` | Create new MBR table |

### Example: Creating a Partition

```bash
$ sudo fdisk /dev/sdb

Command (m for help): n        # New partition
Partition type: p              # Primary
Partition number: 1
First sector: [Enter]          # Default
Last sector: +50G              # 50GB size

Command (m for help): p        # Verify
Command (m for help): w        # Write
```

## Partitioning with `parted`

`parted` handles both MBR and GPT, with immediate changes:

```bash
$ sudo parted /dev/sdb

(parted) print                 # Show partitions
(parted) mklabel gpt           # Create GPT table
(parted) mkpart primary ext4 0% 50%    # Create partition
(parted) print                 # Verify
(parted) quit
```

## Filesystems

After partitioning, format the partition with a filesystem.

### Filesystem Types Comparison

| Filesystem | Max File Size | Max Volume | Features |
|------------|---------------|------------|----------|
| **ext4** | 16 TB | 1 EB | Standard, journaling, stable |
| **XFS** | 8 EB | 8 EB | High performance, scales well |
| **Btrfs** | 16 EB | 16 EB | Snapshots, checksums, CoW |
| **ZFS** | 16 EB | 256 ZB | Enterprise, compression, RAID |
| **NTFS** | 16 TB | 256 TB | Windows compatibility |
| **FAT32** | 4 GB | 2 TB | USB drives, legacy |

### Creating Filesystems

```bash
$ sudo mkfs.ext4 /dev/sdb1           # ext4
$ sudo mkfs.xfs /dev/sdb1            # XFS
$ sudo mkfs.btrfs /dev/sdb1          # Btrfs
$ sudo mkfs.vfat -F 32 /dev/sdb1     # FAT32

# With label
$ sudo mkfs.ext4 -L "DataDisk" /dev/sdb1
```

### Filesystem Information

```bash
$ sudo blkid /dev/sdb1               # UUID and type
$ sudo tune2fs -l /dev/sdb1          # ext4 details
$ sudo xfs_info /dev/sdb1            # XFS details
```

## LVM - Logical Volume Manager

LVM provides flexible disk management with resizable volumes.

### LVM Concepts

```
Physical Volumes (PV)   →   Volume Groups (VG)   →   Logical Volumes (LV)
  /dev/sdb1                     vg_data                 lv_data
  /dev/sdc1                                             lv_backup
```

| Term | Description |
|------|-------------|
| **PV** | Physical Volume - a partition or disk |
| **VG** | Volume Group - pool of PVs |
| **LV** | Logical Volume - "virtual partition" from VG |

### Creating LVM Setup

```bash
# 1. Create Physical Volumes
$ sudo pvcreate /dev/sdb1 /dev/sdc1
$ sudo pvs                            # List PVs

# 2. Create Volume Group
$ sudo vgcreate vg_data /dev/sdb1 /dev/sdc1
$ sudo vgs                            # List VGs

# 3. Create Logical Volume
$ sudo lvcreate -L 100G -n lv_storage vg_data
$ sudo lvs                            # List LVs

# 4. Create filesystem and mount
$ sudo mkfs.ext4 /dev/vg_data/lv_storage
$ sudo mount /dev/vg_data/lv_storage /mnt/storage
```

### Extending LVM

```bash
# Extend Volume Group (add new PV)
$ sudo pvcreate /dev/sdd1
$ sudo vgextend vg_data /dev/sdd1

# Extend Logical Volume
$ sudo lvextend -L +50G /dev/vg_data/lv_storage
# or use all free space
$ sudo lvextend -l +100%FREE /dev/vg_data/lv_storage

# Resize filesystem
$ sudo resize2fs /dev/vg_data/lv_storage    # ext4
$ sudo xfs_growfs /mnt/storage              # XFS
```

### LVM Snapshots

```bash
# Create snapshot
$ sudo lvcreate -L 10G -s -n snap_storage /dev/vg_data/lv_storage

# Mount snapshot (read-only)
$ sudo mount -o ro /dev/vg_data/snap_storage /mnt/snap

# Remove snapshot
$ sudo lvremove /dev/vg_data/snap_storage
```

## Checking and Repairing Filesystems

```bash
# Check filesystem (unmount first!)
$ sudo umount /dev/sdb1
$ sudo fsck /dev/sdb1
$ sudo fsck.ext4 /dev/sdb1

# Check XFS (can check while mounted)
$ sudo xfs_repair /dev/sdb1          # Unmounted
$ sudo xfs_repair -n /dev/sdb1       # Dry run
```

## Hands-On Exercise

1. View current disk layout:
   ```bash
   $ lsblk
   $ df -hT
   $ sudo fdisk -l
   ```

2. Check disk usage:
   ```bash
   $ du -h --max-depth=1 /var | sort -rh | head
   $ df -h /
   ```

3. View filesystem details:
   ```bash
   $ sudo blkid
   $ sudo tune2fs -l /dev/sda1 | grep -E "Block count|Created|UUID"
   ```

4. If you have a spare disk/VM, practice partitioning:
   ```bash
   $ sudo fdisk /dev/sdb
   # Create a new partition
   # Write and exit
   $ sudo mkfs.ext4 /dev/sdb1
   $ sudo mount /dev/sdb1 /mnt
   $ df -h /mnt
   ```
