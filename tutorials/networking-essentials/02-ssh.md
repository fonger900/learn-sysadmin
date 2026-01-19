---
title: 2. SSH (Secure Shell)
date: 2026-01-20
order: 2
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

# Or copy and paste manually
$ cat ~/.ssh/id_ed25519.pub
# Copy output, then on server:
$ vim ~/.ssh/authorized_keys
# Paste the public key
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
$ chmod 644 ~/.ssh/id_ed25519.pub
```

## SSH Client Configuration

### The Config File (`~/.ssh/config`)

Create shortcuts and default settings:

```bash
# ~/.ssh/config

# Default settings for all hosts
Host *
    AddKeysToAgent yes
    IdentitiesOnly yes

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

Host jumphost
    HostName jump.example.com
    User admin

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
$ ssh aws-prod
```

### Useful Config Options

| Option | Description |
|--------|-------------|
| `HostName` | Real hostname or IP |
| `User` | Username |
| `Port` | Non-default port |
| `IdentityFile` | Path to private key |
| `ProxyJump` | Jump through another host |
| `ForwardAgent` | Forward SSH agent |
| `LocalForward` | Port forwarding |
| `ServerAliveInterval` | Keep connection alive |

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
AllowGroups sshusers

# Change default port (security through obscurity)
Port 2222

# Limit authentication attempts
MaxAuthTries 3

# Disable empty passwords
PermitEmptyPasswords no

# Use only SSH protocol 2
Protocol 2
```

Apply changes:
```bash
$ sudo systemctl restart sshd
```

### Test Config Before Restart

```bash
$ sudo sshd -t          # Test config syntax
$ sudo sshd -T          # Show effective config
```

## SSH Tunneling (Port Forwarding)

### Local Port Forwarding

Access remote service through local port:

```bash
# Forward local port 8080 to remote server's localhost:80
$ ssh -L 8080:localhost:80 user@server

# Access remote database through tunnel
$ ssh -L 5432:localhost:5432 user@dbserver
# Now connect to localhost:5432 to reach db

# Forward to a third host
$ ssh -L 8080:internal-server:80 user@jumphost
```

Use case: Access a web app running on a remote server:
```
Browser -> localhost:8080 -> SSH Tunnel -> server:80
```

### Remote Port Forwarding

Expose local service to remote server:

```bash
# Make local port 3000 available on server's port 8080
$ ssh -R 8080:localhost:3000 user@server
```

Use case: Share local dev server with a teammate.

### Dynamic Port Forwarding (SOCKS Proxy)

Create a SOCKS proxy for arbitrary connections:

```bash
$ ssh -D 1080 user@server

# Configure browser to use localhost:1080 as SOCKS proxy
# All traffic goes through the SSH tunnel
```

### Keep Tunnel Open

```bash
# Background tunnel with no shell
$ ssh -fNL 8080:localhost:80 user@server

# -f = background after authentication
# -N = don't execute remote command
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

# With different port
$ scp -P 2222 file.txt user@server:/path/

# Preserve permissions
$ scp -p file.txt user@server:/path/
```

### SFTP (SSH File Transfer Protocol)

Interactive file transfer:

```bash
$ sftp user@server
sftp> ls                  # List remote files
sftp> lls                 # List local files
sftp> cd /var/www         # Change remote directory
sftp> lcd ~/Documents     # Change local directory
sftp> get file.txt        # Download file
sftp> put local.txt       # Upload file
sftp> get -r folder/      # Download directory
sftp> put -r folder/      # Upload directory
sftp> exit
```

### rsync Over SSH

Best for syncing files:

```bash
# Sync local to remote
$ rsync -avz ./folder/ user@server:/path/to/destination/

# Sync remote to local
$ rsync -avz user@server:/path/to/source/ ./folder/

# Delete files that don't exist in source
$ rsync -avz --delete ./folder/ user@server:/destination/

# With different port
$ rsync -avz -e "ssh -p 2222" ./folder/ user@server:/path/
```

| Flag | Description |
|------|-------------|
| `-a` | Archive mode (preserves everything) |
| `-v` | Verbose |
| `-z` | Compress during transfer |
| `--delete` | Delete extraneous files |
| `--progress` | Show progress |

## SSH Agent

Manage keys in memory (avoid retyping passphrase):

```bash
# Start agent
$ eval $(ssh-agent)

# Add key
$ ssh-add ~/.ssh/id_ed25519

# List loaded keys
$ ssh-add -l

# Remove all keys
$ ssh-add -D
```

### Forward Agent (Use Local Keys on Remote)

```bash
$ ssh -A user@jumphost
# Now on jumphost, you can ssh to other servers using your local keys
```

**Warning**: Only use agent forwarding to trusted servers!

## Security Best Practices

1. **Use key authentication, disable passwords**
2. **Protect private keys with passphrases**
3. **Disable root login**: `PermitRootLogin no`
4. **Use strong key types**: ED25519 or RSA-4096
5. **Keep software updated**
6. **Use fail2ban** to block brute force attacks
7. **Change default port** (optional, reduces noise)
8. **Limit user access**: Use `AllowUsers` or `AllowGroups`

## Troubleshooting

### Common Issues

```bash
# Permission denied
$ chmod 600 ~/.ssh/id_ed25519
$ chmod 700 ~/.ssh

# See detailed connection info
$ ssh -vvv user@server

# Check server logs
$ sudo tail -f /var/log/auth.log       # Debian/Ubuntu
$ sudo tail -f /var/log/secure         # RHEL/CentOS

# Test specific key
$ ssh -i ~/.ssh/specific_key user@server
```

### Host Key Changed Warning

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
```

If legitimate (server reinstall):
```bash
$ ssh-keygen -R hostname
```

## Hands-On Exercise

1. Generate an SSH key:
   ```bash
   $ ssh-keygen -t ed25519 -C "your_email@example.com"
   $ ls -la ~/.ssh/
   ```

2. Create SSH config for localhost (for testing):
   ```bash
   $ cat << 'EOF' >> ~/.ssh/config
   Host local
       HostName localhost
       User $(whoami)
   EOF
   ```

3. Check SSH service status:
   ```bash
   $ systemctl status sshd
   ```

4. Test local port forward:
   ```bash
   # In one terminal, start simple HTTP server
   $ python3 -m http.server 8000
   
   # In another, forward port 9000 to 8000
   $ ssh -L 9000:localhost:8000 localhost
   
   # Access http://localhost:9000
   ```

5. Practice file transfer:
   ```bash
   $ echo "test" > /tmp/testfile.txt
   $ scp /tmp/testfile.txt localhost:/tmp/testfile2.txt
   ```
