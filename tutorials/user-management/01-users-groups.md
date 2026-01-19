---
title: 1. Users and Groups
date: 2026-01-20
order: 1
---
# Users and Groups

Linux is a multi-user operating system. Understanding how users and groups work is essential for security and access control.

## Core Concepts

### Users
Every user has:
- **Username**: Human-readable identifier (e.g., `alice`)
- **UID**: Unique numeric User ID
- **Home directory**: Personal storage (usually `/home/username`)
- **Default shell**: The shell started on login

### Groups
Groups allow managing permissions for multiple users:
- **Primary group**: Assigned when user is created
- **Secondary groups**: Additional group memberships
- Every file/directory has an owner user AND owner group

## User ID Ranges

| UID Range | Type | Examples |
|-----------|------|----------|
| `0` | Root (superuser) | `root` |
| `1-999` | System users | `www-data`, `mysql`, `nobody` |
| `1000+` | Regular users | `alice`, `bob` |

Check your UID:
```bash
$ id
uid=1000(alice) gid=1000(alice) groups=1000(alice),27(sudo),docker(998)
```

## Important Files

### `/etc/passwd` - User Database
Contains user account information (readable by everyone):
```
username:x:UID:GID:comment:home:shell
```

```bash
$ cat /etc/passwd | grep alice
alice:x:1000:1000:Alice Smith:/home/alice:/bin/bash
```

| Field | Description |
|-------|-------------|
| `username` | Login name |
| `x` | Password placeholder (in `/etc/shadow`) |
| `UID` | User ID |
| `GID` | Primary group ID |
| `comment` | Full name or description (GECOS) |
| `home` | Home directory |
| `shell` | Default login shell |

### `/etc/shadow` - Password Storage
Contains encrypted passwords (root-readable only):
```
username:$6$...:18500:0:99999:7:::
```

| Field | Description |
|-------|-------------|
| `$6$...` | Encrypted password (SHA-512) |
| `18500` | Days since Jan 1, 1970 password was changed |
| `0` | Min days before password can change |
| `99999` | Max days before password must change |
| `7` | Warning days before expiration |

### `/etc/group` - Group Database
```
groupname:x:GID:member1,member2
```

```bash
$ cat /etc/group | grep sudo
sudo:x:27:alice,bob
```

## Managing Users

### Creating Users
```bash
# Create user with defaults
$ sudo useradd alice

# Create user with home directory and shell
$ sudo useradd -m -s /bin/bash alice

# Create user with specific UID
$ sudo useradd -u 1500 alice

# Create user and add to groups
$ sudo useradd -m -G sudo,docker alice
```

| Option | Description |
|--------|-------------|
| `-m` | Create home directory |
| `-s /bin/bash` | Set login shell |
| `-u 1500` | Set specific UID |
| `-G grp1,grp2` | Add to secondary groups |
| `-c "Full Name"` | Set comment (full name) |
| `-e 2025-12-31` | Account expiration date |

### Setting Passwords
```bash
$ sudo passwd alice       # Set password for alice
$ passwd                  # Change your own password
$ sudo passwd -l alice    # Lock account
$ sudo passwd -u alice    # Unlock account
```

### Modifying Users
```bash
$ sudo usermod -aG docker alice    # Add to group (important: -a!)
$ sudo usermod -s /bin/zsh alice   # Change shell
$ sudo usermod -l newname alice    # Change username
$ sudo usermod -L alice            # Lock account
$ sudo usermod -U alice            # Unlock account
```

> **WARNING**: Always use `-aG` (append) when adding groups. Using just `-G` replaces all secondary groups!

### Deleting Users
```bash
$ sudo userdel alice           # Delete user only
$ sudo userdel -r alice        # Delete user + home directory
```

## Managing Groups

### Creating Groups
```bash
$ sudo groupadd developers
$ sudo groupadd -g 2000 webteam   # With specific GID
```

### Adding Users to Groups
```bash
$ sudo usermod -aG developers alice   # Add to group
$ sudo gpasswd -a alice developers    # Alternative method
```

### Viewing Group Membership
```bash
$ groups                    # Your groups
$ groups alice              # Alice's groups
$ id alice                  # Detailed info
$ getent group developers   # Members of group
```

### Removing Users from Groups
```bash
$ sudo gpasswd -d alice developers
```

### Deleting Groups
```bash
$ sudo groupdel developers
```

## Switching Users

```bash
$ su alice          # Switch to alice (needs password)
$ su - alice        # Switch with login shell (loads environment)
$ sudo su -         # Switch to root
$ exit              # Return to previous user
```

## System Users

System users run services without login capability:

```bash
# Create system user for a service
$ sudo useradd -r -s /usr/sbin/nologin myservice

# Common system users
$ cat /etc/passwd | grep -E "www-data|mysql|postgres"
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

## Best Practices

1. **Never log in as root** - Use `sudo` instead
2. **Use strong passwords** - Enforce with `pam_pwquality`
3. **Review `/etc/passwd` regularly** - Check for unauthorized accounts
4. **Remove unused accounts** - `userdel -r olduser`
5. **Use groups for access control** - Easier than per-user permissions
6. **Set password expiration** - `chage -M 90 username`

## Hands-On Exercise

1. Create a new user:
   ```bash
   $ sudo useradd -m -s /bin/bash testuser
   $ sudo passwd testuser
   ```

2. View user information:
   ```bash
   $ id testuser
   $ grep testuser /etc/passwd
   ```

3. Create a group and add the user:
   ```bash
   $ sudo groupadd testgroup
   $ sudo usermod -aG testgroup testuser
   $ groups testuser
   ```

4. Switch to the new user:
   ```bash
   $ su - testuser
   $ whoami
   $ pwd
   $ exit
   ```

5. Clean up:
   ```bash
   $ sudo userdel -r testuser
   $ sudo groupdel testgroup
   ```
