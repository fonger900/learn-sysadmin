---
title: 2. File Permissions
date: 2026-01-20
order: 2
---
# File Permissions

Linux file permissions control who can read, write, and execute files and directories. Understanding permissions is crucial for security.

## Viewing Permissions

Use `ls -l` to see permissions:
```bash
$ ls -l /etc/passwd
-rw-r--r-- 1 root root 2847 Jan 15 10:30 /etc/passwd
```

Breaking down `-rw-r--r--`:
```
-    rw-    r--    r--
│     │      │      │
│     │      │      └── Others (everyone else)
│     │      └── Group
│     └── User (owner)
└── File type (- = file, d = directory, l = link)
```

## Permission Types

| Symbol | Permission | For Files | For Directories |
|--------|------------|-----------|-----------------|
| `r` | Read (4) | View contents | List contents |
| `w` | Write (2) | Modify contents | Create/delete files |
| `x` | Execute (1) | Run as program | Enter directory |
| `-` | None (0) | No permission | No permission |

### Directory Permissions Explained

| Permission | Effect on Directory |
|------------|---------------------|
| `r` only | Can list files, but not access them |
| `x` only | Can access files if you know the name |
| `r + x` | Can list and access files (normal read access) |
| `w + x` | Can create, delete, and rename files |

## Numeric (Octal) Permissions

Calculate by adding values:
- Read = 4
- Write = 2
- Execute = 1

| Numeric | Symbolic | Meaning |
|---------|----------|---------|
| `7` | `rwx` | Read + Write + Execute |
| `6` | `rw-` | Read + Write |
| `5` | `r-x` | Read + Execute |
| `4` | `r--` | Read only |
| `3` | `-wx` | Write + Execute |
| `2` | `-w-` | Write only |
| `1` | `--x` | Execute only |
| `0` | `---` | No permissions |

### Common Permission Sets

| Numeric | Symbolic | Use Case |
|---------|----------|----------|
| `755` | `rwxr-xr-x` | Directories, executables |
| `644` | `rw-r--r--` | Regular files |
| `600` | `rw-------` | Private files |
| `700` | `rwx------` | Private executables/directories |
| `777` | `rwxrwxrwx` | ⚠️ Everyone can do everything |
| `666` | `rw-rw-rw-` | ⚠️ Everyone can read/write |

## Changing Permissions with `chmod`

### Numeric Method
```bash
$ chmod 755 script.sh         # rwxr-xr-x
$ chmod 644 file.txt          # rw-r--r--
$ chmod 600 secret.key        # rw-------
$ chmod -R 755 directory/     # Recursive
```

### Symbolic Method
Syntax: `chmod [who][operator][permission]`

**Who:**
- `u` = user (owner)
- `g` = group
- `o` = others
- `a` = all (u + g + o)

**Operator:**
- `+` = add permission
- `-` = remove permission
- `=` = set exact permission

```bash
$ chmod u+x script.sh         # Add execute for owner
$ chmod g-w file.txt          # Remove write from group
$ chmod o= file.txt           # Remove all permissions for others
$ chmod a+r readme.txt        # Add read for everyone
$ chmod u=rwx,g=rx,o=r file   # Set specific permissions
```

## Changing Ownership with `chown`

```bash
$ sudo chown alice file.txt           # Change owner
$ sudo chown alice:developers file.txt # Change owner and group
$ sudo chown :developers file.txt     # Change group only
$ sudo chown -R alice:alice ~/project # Recursive
```

## Changing Group with `chgrp`

```bash
$ sudo chgrp developers file.txt
$ sudo chgrp -R webteam /var/www
```

## Special Permissions

Beyond the standard permissions, Linux has three special permission bits:

### 1. SUID (Set User ID) - `4xxx` or `s`
When set on an executable, it runs with the **owner's** privileges:

```bash
$ ls -l /usr/bin/passwd
-rwsr-xr-x 1 root root 68208 Jan 15 /usr/bin/passwd
   ^
   └── 's' instead of 'x' = SUID is set
```

The `passwd` command needs root access to modify `/etc/shadow`, so it has SUID.

```bash
$ chmod u+s executable        # Set SUID
$ chmod 4755 executable       # Set SUID numerically
$ find / -perm -4000 2>/dev/null   # Find all SUID files
```

### 2. SGID (Set Group ID) - `2xxx` or `s`
**On files**: Runs with group's privileges  
**On directories**: New files inherit the directory's group

```bash
$ chmod g+s shared_dir/       # Set SGID on directory
$ chmod 2775 shared_dir/      # Set SGID numerically

# Example: shared project folder
$ sudo mkdir /projects/team
$ sudo chown :developers /projects/team
$ sudo chmod 2775 /projects/team
# Now all new files will belong to 'developers' group
```

### 3. Sticky Bit - `1xxx` or `t`
Only the file owner can delete files in the directory:

```bash
$ ls -ld /tmp
drwxrwxrwt 1 root root 4096 Jan 15 /tmp
         ^
         └── 't' = sticky bit
```

Everyone can create files in `/tmp`, but only delete their own.

```bash
$ chmod +t directory/         # Set sticky bit
$ chmod 1777 directory/       # Set sticky bit numerically
```

### Special Permissions Summary

| Permission | Numeric | Symbolic | Effect |
|------------|---------|----------|--------|
| SUID | `4xxx` | `u+s` | Execute as file owner |
| SGID | `2xxx` | `g+s` | Execute as group / inherit group |
| Sticky | `1xxx` | `+t` | Only owner can delete |

## Default Permissions: `umask`

The `umask` determines default permissions for new files:

```bash
$ umask
0022

$ umask -S
u=rwx,g=rx,o=rx
```

**How umask works:**
- Maximum permissions: Files = 666, Directories = 777
- Actual permissions = Maximum - umask

| umask | File Permissions | Directory Permissions |
|-------|------------------|----------------------|
| `022` | 644 (rw-r--r--) | 755 (rwxr-xr-x) |
| `077` | 600 (rw-------) | 700 (rwx------) |
| `002` | 664 (rw-rw-r--) | 775 (rwxrwxr-x) |

Set umask for the session:
```bash
$ umask 077                   # Private files
```

Set permanently in `~/.bashrc`:
```bash
umask 022
```

## Access Control Lists (ACLs)

ACLs provide fine-grained permissions beyond user/group/others:

### Check ACL Support
```bash
$ mount | grep acl
$ tune2fs -l /dev/sda1 | grep "Default mount options"
```

### View ACLs
```bash
$ getfacl file.txt
# file: file.txt
# owner: alice
# group: users
user::rw-
group::r--
other::r--
```

### Set ACLs
```bash
# Give bob read/write access
$ setfacl -m u:bob:rw file.txt

# Give developers group read access
$ setfacl -m g:developers:r file.txt

# Set default ACL for directory (new files inherit)
$ setfacl -d -m g:developers:rwx /projects/

# Remove ACL entries
$ setfacl -x u:bob file.txt

# Remove all ACLs
$ setfacl -b file.txt
```

A `+` in `ls -l` indicates ACLs are set:
```bash
$ ls -l file.txt
-rw-rw-r--+ 1 alice users 0 Jan 15 file.txt
          ^
          └── ACL is set
```

## Hands-On Exercise

1. Create a test file and view permissions:
   ```bash
   $ touch testfile.txt
   $ ls -l testfile.txt
   ```

2. Change permissions using both methods:
   ```bash
   $ chmod 755 testfile.txt
   $ ls -l testfile.txt
   $ chmod u=rw,g=r,o= testfile.txt
   $ ls -l testfile.txt
   ```

3. Create a shared directory with SGID:
   ```bash
   $ mkdir shared_folder
   $ chmod 2775 shared_folder
   $ ls -ld shared_folder
   ```

4. Check your current umask:
   ```bash
   $ umask
   $ touch newfile.txt
   $ ls -l newfile.txt
   ```

5. Practice ACLs (if available):
   ```bash
   $ setfacl -m u:nobody:r testfile.txt
   $ getfacl testfile.txt
   $ setfacl -b testfile.txt
   ```
