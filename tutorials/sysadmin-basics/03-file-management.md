---
title: 3. File Management
date: 2026-01-20
order: 3
---
# File Management

## Creating Files and Directories
- `touch file.txt`: Create an empty file
- `mkdir myfolder`: Create a directory
- `mkdir -p parent/child`: Create nested directories

## Copying and Moving
- `cp source dest`: Copy file
- `cp -r sourcedir destdir`: Copy directory recursively
- `mv source dest`: Move or rename file

## Deleting
- `rm file`: Remove file
- `rm -r directory`: Remove directory
- **WARNING**: `rm -rf /` will destroy your system.

## Viewing Content
- `cat file`: Output entire file content
- `less file`: View file with pagination using arrow keys
- `head file`: View first 10 lines
- `tail file`: View last 10 lines
