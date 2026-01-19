---
title: 1. Partitions and Filesystems
date: 2026-01-20
order: 1
---
# Partitions and Filesystems

## Disks
Identified as `/dev/sda` (first disk), `/dev/sdb`, etc., or `/dev/nvme0n1` (NVMe).

## Partitioning
Dividing a physical disk into logical sections (e.g., `/dev/sda1`).
- `lsblk`: List block devices
- `fdisk /dev/sda`: MBR partitioning tool
- `gdisk /dev/sda`: GPT partitioning tool

## Filesystems
Formatting a partition so files can be stored.
- `ext4`: Standard Linux filesystem
- `xfs`: High performance
- `mkfs.ext4 /dev/sda1`: Create ext4 filesystem on partition 1
