---
title: 6. SSH (Secure Shell)
order: 6
date: 2026-02-06
---
# SSH (Secure Shell)

SSH is the standard protocol for secure remote administration. It provides encrypted communication for command-line access, file transfers, and port forwarding.

## SSH Basics

### Connecting to a Remote Server

```bash
# Basic connection (will prompt for password)
$ ssh username@hostname
$ ssh user@192.168.1.100

# Connect on different port
$ ssh -p 2222 user@hostname

# With verbose output (for debugging)
$ ssh -v user@hostname
```

### First Connection

On first connect, you'll see:
```
The authenticity of host 'server (192.168.1.100)' can't be established.
ED25519 key fingerprint is SHA256:abc123...
Are you sure you want to continue connecting (yes/no)?
```

Type `yes` to add the server to your known hosts (`~/.ssh/known_hosts`).

## Key-Based Authentication

SSH keys are more secure than passwords and enable passwordless login.

### How It Works

```
┌─────────────────┐         ┌─────────────────┐
│    Client       │         │     Server      │
│                 │         │                 │
│  Private Key    │  ===>   │  Public Key     │
│  (id_ed25519)   │  Auth   │  (authorized_   │
│  KEEP SECRET!   │         │   keys)         │
└─────────────────┘         └─────────────────┘
```

### Generate SSH Key Pair

```bash
# Generate ED25519 key (recommended)
$ ssh-keygen -t ed25519 -C "your_email@example.com"

# Generate RSA key (legacy compatibility)
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Will prompt for:
# - File location (default: ~/.ssh/id_ed25519)
# - Passphrase (recommended for security)
```

### Key Types

| Type | Security | Speed | Compatibility |
|------|----------|-------|---------------|
| **ed25519** | Excellent | Fast | Modern systems |
| **rsa (4096)** | Good | Slower | Universal |
| **ecdsa** | Good | Fast | Wide support |

### Copy Public Key to Server

```bash
# Automatic method (recommended)
$ ssh-copy-id user@hostname

# Manual method
$ cat ~/.ssh/id_ed25519.pub | ssh user@hostname "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

### Key Files and Permissions

```bash
~/.ssh/
├── id_ed25519          # Private key (chmod 600)
├── id_ed25519.pub      # Public key (chmod 644)
├── authorized_keys     # Server: allowed public keys (chmod 600)
├── known_hosts         # Known server fingerprints (chmod 644)
└── config              # Client configuration (chmod 600)
```

**Critical permissions:**
```bash
$ chmod 700 ~/.ssh
$ chmod 600 ~/.ssh/id_ed25519
$ chmod 600 ~/.ssh/authorized_keys
```

## SSH Client Configuration

### The Config File (`~/.ssh/config`)

Create shortcuts and default settings:

```bash
# ~/.ssh/config

# Web server shortcut
Host webserver
    HostName 192.168.1.100
    User admin
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# Jump host example
Host production
    HostName 10.0.0.50
    User deploy
    ProxyJump jumphost

# AWS EC2 instance
Host aws-prod
    HostName ec2-1-2-3-4.compute.amazonaws.com
    User ec2-user
    IdentityFile ~/.ssh/aws-key.pem
```

Now connect with just:
```bash
$ ssh webserver
$ ssh production
```

## SSH Server Configuration

### Server Config (`/etc/ssh/sshd_config`)

Key security settings:

```bash
# Disable password authentication (after setting up keys!)
PasswordAuthentication no

# Disable root login
PermitRootLogin no

# Limit users
AllowUsers alice bob

# Change default port
Port 2222

# Limit authentication attempts
MaxAuthTries 3
```

Apply changes:
```bash
$ sudo systemctl restart sshd
```

## SSH Tunneling (Port Forwarding)

### Local Port Forwarding

Access remote service through local port:

```bash
# Forward local port 8080 to remote server's localhost:80
$ ssh -L 8080:localhost:80 user@server

# Access remote database through tunnel
$ ssh -L 5432:localhost:5432 user@dbserver
```

### Remote Port Forwarding

Expose local service to remote server:

```bash
# Make local port 3000 available on server's port 8080
$ ssh -R 8080:localhost:3000 user@server
```

### Dynamic Port Forwarding (SOCKS Proxy)

```bash
$ ssh -D 1080 user@server
# Configure browser to use localhost:1080 as SOCKS proxy
```

## File Transfer

### SCP (Secure Copy)

```bash
# Copy file to remote
$ scp file.txt user@server:/path/to/destination/

# Copy file from remote
$ scp user@server:/path/to/file.txt ./

# Copy directory recursively
$ scp -r ./folder user@server:/path/
```

### SFTP (SSH File Transfer Protocol)

```bash
$ sftp user@server
sftp> ls                  # List remote files
sftp> get file.txt        # Download file
sftp> put local.txt       # Upload file
sftp> exit
```

### rsync Over SSH

```bash
$ rsync -avzP /local/path/ user@server:/remote/path/
$ rsync -avzP user@server:/remote/path/ /local/path/
```

## Security Best Practices

1. **Use key authentication, disable passwords**
2. **Protect private keys with passphrases**
3. **Disable root login**: `PermitRootLogin no`
4. **Use strong key types**: ED25519 or RSA-4096
5. **Use fail2ban** to block brute force attacks

## Hands-On Exercise

1. Generate an SSH key:
   ```bash
   $ ssh-keygen -t ed25519 -C "your_email@example.com"
   $ ls -la ~/.ssh/
   ```

2. Check SSH service status:
   ```bash
   $ systemctl status sshd
   ```

3. Test local port forward:
   ```bash
   $ python3 -m http.server 8000 &
   $ ssh -L 9000:localhost:8000 localhost
   # Access http://localhost:9000
   ```
