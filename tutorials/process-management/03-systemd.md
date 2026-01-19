---
title: 3. Services (Systemd)
date: 2026-01-20
order: 3
---
# Systemd Services

Most modern Linux distributions use **systemd** as the init system and service manager. It starts and manages background services (daemons), handles system boot, and more.

## What is Systemd?

Systemd is:
- The first process started at boot (PID 1)
- Manages services (web servers, databases, etc.)
- Handles system targets (similar to runlevels)
- Provides logging (journald)
- Manages mounts, timers, sockets, and more

## Systemctl - The Main Command

`systemctl` is used to control systemd and manage services.

### Basic Service Commands

| Command | Description |
|---------|-------------|
| `systemctl start service` | Start a service |
| `systemctl stop service` | Stop a service |
| `systemctl restart service` | Stop then start |
| `systemctl reload service` | Reload configuration (if supported) |
| `systemctl status service` | Show service status |
| `systemctl enable service` | Enable at boot |
| `systemctl disable service` | Disable at boot |
| `systemctl is-active service` | Check if running |
| `systemctl is-enabled service` | Check if enabled at boot |

### Examples

```bash
$ sudo systemctl start nginx
$ sudo systemctl stop nginx
$ sudo systemctl restart nginx
$ sudo systemctl reload nginx       # Reload config without restart
$ sudo systemctl status nginx

$ sudo systemctl enable nginx       # Start at boot
$ sudo systemctl disable nginx      # Don't start at boot
$ sudo systemctl enable --now nginx # Enable AND start now
```

### Understanding Status Output

```bash
$ systemctl status nginx
● nginx.service - A high performance web server
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 10:30:00 UTC; 1 day ago
       Docs: man:nginx(8)
    Process: 1234 ExecStart=/usr/sbin/nginx -g daemon on; (code=exited, status=0/SUCCESS)
   Main PID: 1235 (nginx)
      Tasks: 3 (limit: 4694)
     Memory: 10.5M
        CPU: 500ms
     CGroup: /system.slice/nginx.service
             ├─1235 nginx: master process /usr/sbin/nginx -g daemon on;
             └─1236 nginx: worker process
```

| Field | Description |
|-------|-------------|
| Loaded | Path and enabled status |
| Active | Running status and uptime |
| Main PID | Main process ID |
| Tasks | Thread count |
| Memory | Memory usage |
| CGroup | Control group hierarchy |

### Listing Services

```bash
$ systemctl list-units --type=service           # Active services
$ systemctl list-units --type=service --all     # All services
$ systemctl list-unit-files --type=service      # All installed services
$ systemctl list-units --failed                 # Failed services
```

## Unit Files

Systemd uses unit files to configure services. 

### Unit File Locations

| Path | Description |
|------|-------------|
| `/lib/systemd/system/` | Package-provided units (don't edit) |
| `/etc/systemd/system/` | Administrator overrides (edit these) |
| `/run/systemd/system/` | Runtime units (temporary) |

Priority: `/etc/` > `/run/` > `/lib/`

### Unit File Structure

A typical service unit file:

```ini
[Unit]
Description=My Application Service
Documentation=https://example.com/docs
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=myapp
Group=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Section Breakdown

**[Unit] Section:**
| Directive | Description |
|-----------|-------------|
| `Description` | Human-readable description |
| `Documentation` | URLs for documentation |
| `After` | Start after these units |
| `Before` | Start before these units |
| `Requires` | Hard dependencies (fail if missing) |
| `Wants` | Soft dependencies |

**[Service] Section:**
| Directive | Description |
|-----------|-------------|
| `Type` | simple, forking, oneshot, notify |
| `ExecStart` | Command to start |
| `ExecStop` | Command to stop |
| `ExecReload` | Command to reload |
| `Restart` | When to restart (always, on-failure) |
| `RestartSec` | Delay before restart |
| `User` / `Group` | Run as user/group |
| `WorkingDirectory` | Working directory |
| `Environment` | Environment variables |
| `EnvironmentFile` | File with environment variables |

**[Install] Section:**
| Directive | Description |
|-----------|-------------|
| `WantedBy` | Target that pulls in this service |
| `RequiredBy` | Target that requires this service |

### Service Types

| Type | Description |
|------|-------------|
| `simple` | Default. ExecStart is the main process |
| `forking` | Forks and parent exits (traditional daemons) |
| `oneshot` | One-time task (for scripts) |
| `notify` | Sends notification when ready |
| `idle` | Waits until other jobs finish |

## Creating a Custom Service

### Example: Node.js Application

1. **Create the unit file:**
```bash
$ sudo vim /etc/systemd/system/myapp.service
```

```ini
[Unit]
Description=My Node.js Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/myapp
ExecStart=/usr/bin/node /var/www/myapp/server.js
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

2. **Reload systemd:**
```bash
$ sudo systemctl daemon-reload
```

3. **Start and enable:**
```bash
$ sudo systemctl start myapp
$ sudo systemctl enable myapp
$ sudo systemctl status myapp
```

## Editing Existing Services

Never edit files in `/lib/systemd/system/`. Instead, create an override:

```bash
$ sudo systemctl edit nginx
```

This creates `/etc/systemd/system/nginx.service.d/override.conf`:

```ini
[Service]
# Example: Increase limits
LimitNOFILE=65536
```

To replace the entire file:
```bash
$ sudo systemctl edit --full nginx
```

After editing, reload:
```bash
$ sudo systemctl daemon-reload
$ sudo systemctl restart nginx
```

## Systemd Targets

Targets are like runlevels in older init systems.

| Target | Equivalent Runlevel | Description |
|--------|---------------------|-------------|
| `poweroff.target` | 0 | System shutdown |
| `rescue.target` | 1 | Single-user mode |
| `multi-user.target` | 3 | Multi-user, no GUI |
| `graphical.target` | 5 | Multi-user with GUI |
| `reboot.target` | 6 | Reboot |

### Manage Targets
```bash
$ systemctl get-default                    # Current default target
$ sudo systemctl set-default multi-user.target   # Set default
$ sudo systemctl isolate multi-user.target       # Switch now
```

## Journalctl - Viewing Logs

Systemd's logging system is called journald, accessed via `journalctl`.

### Basic Usage

```bash
$ journalctl                          # All logs
$ journalctl -b                       # Current boot only
$ journalctl -b -1                    # Previous boot
$ journalctl -u nginx                 # Specific service
$ journalctl -u nginx -u mysql        # Multiple services
$ journalctl -f                       # Follow (like tail -f)
$ journalctl -n 50                    # Last 50 lines
```

### Filtering by Time

```bash
$ journalctl --since "1 hour ago"
$ journalctl --since "2024-01-15"
$ journalctl --since "2024-01-15 10:00" --until "2024-01-15 12:00"
$ journalctl --since yesterday
$ journalctl --since today
```

### Filtering by Priority

| Priority | Level |
|----------|-------|
| 0 | emerg |
| 1 | alert |
| 2 | crit |
| 3 | err |
| 4 | warning |
| 5 | notice |
| 6 | info |
| 7 | debug |

```bash
$ journalctl -p err                   # Errors and above
$ journalctl -p warning -u nginx      # Warnings from nginx
```

### Output Formats

```bash
$ journalctl -o json                  # JSON format
$ journalctl -o json-pretty           # Pretty JSON
$ journalctl -o short-precise         # Precise timestamps
$ journalctl --no-pager               # Don't use pager
```

### Managing Journal

```bash
$ journalctl --disk-usage             # Space used
$ sudo journalctl --rotate            # Force log rotation
$ sudo journalctl --vacuum-time=7d    # Delete logs older than 7 days
$ sudo journalctl --vacuum-size=500M  # Keep only 500MB
```

## Troubleshooting Services

### Check for failures
```bash
$ systemctl --failed
```

### View logs for failed service
```bash
$ journalctl -xeu nginx.service
```
`-x` adds helpful messages, `-e` jumps to end.

### Analyze boot time
```bash
$ systemd-analyze                     # Total boot time
$ systemd-analyze blame               # Time per unit
$ systemd-analyze critical-chain      # Chain of dependencies
```

## Hands-On Exercise

1. Check status of common services:
   ```bash
   $ systemctl status sshd
   $ systemctl status cron
   $ systemctl list-units --type=service | head -20
   ```

2. View logs:
   ```bash
   $ journalctl -u ssh --since "1 hour ago"
   $ journalctl -p err -b
   ```

3. Create a simple service:
   ```bash
   $ cat << 'EOF' | sudo tee /etc/systemd/system/hello.service
   [Unit]
   Description=Hello World Service
   
   [Service]
   Type=oneshot
   ExecStart=/bin/echo "Hello from systemd!"
   
   [Install]
   WantedBy=multi-user.target
   EOF
   
   $ sudo systemctl daemon-reload
   $ sudo systemctl start hello
   $ journalctl -u hello
   ```

4. Analyze boot:
   ```bash
   $ systemd-analyze
   $ systemd-analyze blame | head -10
   ```

5. Clean up:
   ```bash
   $ sudo rm /etc/systemd/system/hello.service
   $ sudo systemctl daemon-reload
   ```
