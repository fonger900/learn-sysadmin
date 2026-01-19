---
title: 4. Viewing File Content
date: 2026-01-04
---
# Viewing File Content

## `cat`
Concatenate and display file content. Good for short files.
```bash
$ cat /etc/hostname
```

## `less`
View file content one screen at a time. Scroll with arrow keys, quit with `q`.
```bash
$ less /var/log/syslog
```

## `head` & `tail`
View the very beginning or end of a file.
```bash
$ head -n 5 report.txt
$ tail -f /var/log/syslog
```
