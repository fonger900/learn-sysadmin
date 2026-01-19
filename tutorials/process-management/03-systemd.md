---
title: 3. Services (Systemd)
date: 2026-01-20
order: 3
---
# Systemd Services

Most modern Linux distros use `systemd` to manage background services (daemons).

## Systemctl
The main command to control systemd.

- `systemctl start apache2`: Start a service
- `systemctl stop apache2`: Stop a service
- `systemctl restart apache2`: Restart
- `systemctl status apache2`: Check status
- `systemctl enable apache2`: Enable service to start at boot
- `systemctl disable apache2`: Disable service from starting at boot
