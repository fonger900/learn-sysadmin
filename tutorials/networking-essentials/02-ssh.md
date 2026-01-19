---
title: 2. SSH (Secure Shell)
date: 2026-01-20
order: 2
---
# SSH

The standard for remote administration.

## Client
- `ssh user@hostname`: Connect to remote host
- `ssh -i key.pem user@host`: Connect using identity file

## Server Configuration
Located at `/etc/ssh/sshd_config`.
- `PasswordAuthentication no`: Disable password login (use keys!)
- `PermitRootLogin no`: Security best practice
- `systemctl restart ssh`: Apply changes

## Key-Based Authentication
1. Generate key pair: `ssh-keygen`
2. Copy public key to server: `ssh-copy-id user@host`
