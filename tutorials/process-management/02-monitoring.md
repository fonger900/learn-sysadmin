---
title: 2. Managing Processes
date: 2026-01-20
order: 2
---
# Managing Processes

Sometimes processes misbehave, consume too many resources, or need to be stopped. This tutorial covers how to control and manage running processes.

## Signals

Signals are software interrupts used to communicate with processes. They can tell a process to terminate, pause, continue, or perform other actions.

### Common Signals

| Signal | Number | Description | Can be caught? |
|--------|--------|-------------|----------------|
| `SIGHUP` | 1 | Hangup - reload configuration | Yes |
| `SIGINT` | 2 | Interrupt (Ctrl+C) | Yes |
| `SIGQUIT` | 3 | Quit with core dump | Yes |
| `SIGKILL` | 9 | Force kill immediately | **No** |
| `SIGTERM` | 15 | Graceful termination (default) | Yes |
| `SIGSTOP` | 19 | Stop (pause) process | **No** |
| `SIGCONT` | 18 | Continue stopped process | Yes |
| `SIGUSR1` | 10 | User-defined signal 1 | Yes |
| `SIGUSR2` | 12 | User-defined signal 2 | Yes |

### SIGTERM vs SIGKILL

| SIGTERM (15) | SIGKILL (9) |
|--------------|-------------|
| Asks process to terminate | Forces immediate termination |
| Process can clean up | No cleanup possible |
| Can be caught/ignored | Cannot be caught/ignored |
| **Always try first** | Last resort |

**Best practice:** Always try `SIGTERM` first, wait a few seconds, then use `SIGKILL` only if necessary.

## The `kill` Command

Despite its name, `kill` sends **any** signal to a process.

### Syntax
```bash
$ kill [signal] PID
$ kill -SIGNAL PID
$ kill -s SIGNAL PID
```

### Examples
```bash
$ kill 1234              # Send SIGTERM (default) to PID 1234
$ kill -15 1234          # Same as above (explicit)
$ kill -TERM 1234        # Same as above (by name)

$ kill -9 1234           # Send SIGKILL - force kill
$ kill -KILL 1234        # Same as above

$ kill -1 1234           # Send SIGHUP - reload config
$ kill -HUP 1234         # Same as above

$ kill -STOP 1234        # Pause process
$ kill -CONT 1234        # Resume process
```

### List Available Signals
```bash
$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL
 5) SIGTRAP      6) SIGABRT      7) SIGBUS       8) SIGFPE
 9) SIGKILL     10) SIGUSR1     11) SIGSEGV     12) SIGUSR2
...
```

## Process Lookup Commands

### `pgrep` - Find Processes by Name/Pattern

```bash
$ pgrep nginx                   # PIDs of all nginx processes
$ pgrep -l nginx                # PIDs with names
$ pgrep -a nginx                # PIDs with full command
$ pgrep -u root nginx           # Nginx processes owned by root
$ pgrep -c nginx                # Count of matching processes
$ pgrep -f "python script.py"   # Match full command line
```

### `pidof` - Find PID of a Program

```bash
$ pidof nginx                   # PIDs of nginx (space-separated)
$ pidof -s nginx                # Single PID only
```

### Difference Table

| Command | Matches | Output |
|---------|---------|--------|
| `pgrep nginx` | Process name pattern | One PID per line |
| `pidof nginx` | Exact program name | PIDs space-separated |

## Mass Kill Commands

### `killall` - Kill by Name

```bash
$ killall firefox               # Kill all firefox processes
$ killall -9 firefox            # Force kill all firefox
$ killall -u alice              # Kill all processes by user alice
$ killall -i firefox            # Interactive (confirm each)
$ killall -w firefox            # Wait for processes to die
```

### `pkill` - Kill by Pattern

```bash
$ pkill nginx                   # Kill by name
$ pkill -9 nginx                # Force kill
$ pkill -u alice                # Kill user's processes
$ pkill -f "python script.py"   # Kill by full command line
$ pkill -t pts/0                # Kill processes on terminal pts/0
```

### Summary

| Command | Matches by | Use case |
|---------|------------|----------|
| `kill PID` | PID | Specific process |
| `killall name` | Exact name | All instances of program |
| `pkill pattern` | Name pattern | Flexible matching |

## Investigating Processes

### `lsof` - List Open Files

Since "everything is a file" in Linux, this is incredibly powerful:

```bash
# Files opened by a process
$ lsof -p 1234

# Processes using a file
$ lsof /var/log/syslog

# Network connections
$ lsof -i                       # All network connections
$ lsof -i :80                   # Processes on port 80
$ lsof -i :443                  # Processes on port 443
$ lsof -i tcp                   # TCP connections only
$ lsof -i @192.168.1.1          # Connections to specific host

# Files opened by user
$ lsof -u alice

# Processes in a directory
$ lsof +D /var/log/
```

### `fuser` - Find Process Using File/Port

```bash
$ fuser /var/log/syslog         # PIDs using the file
$ fuser -v /var/log/syslog      # Verbose with details
$ fuser -k /var/log/syslog      # Kill processes using file

# Find what's using a port
$ fuser -n tcp 80               # Processes on port 80
$ fuser -vn tcp 80              # Verbose
```

### `strace` - Trace System Calls

For debugging what a process is doing:

```bash
$ strace -p 1234                # Attach to running process
$ strace ls                     # Trace a command
$ strace -f command             # Follow child processes
$ strace -e open command        # Only trace 'open' calls
$ strace -o output.txt command  # Save to file
```

## Managing Unresponsive Processes

### Step-by-step troubleshooting

1. **Try graceful termination:**
   ```bash
   $ kill 1234              # SIGTERM
   $ sleep 5
   ```

2. **Check if process is gone:**
   ```bash
   $ ps -p 1234
   ```

3. **If still running, force kill:**
   ```bash
   $ kill -9 1234           # SIGKILL
   ```

4. **If process is "D" state (uninterruptible sleep):**
   - Usually waiting for I/O
   - Cannot be killed, even with SIGKILL
   - May indicate hardware issue (failed disk)
   - May require system reboot

### Zombie Processes

Zombies can't be killed (already dead), only reaped. Kill or restart the parent:

```bash
# Find zombies
$ ps aux | grep 'Z'

# Find parent of zombie
$ ps -o ppid= -p <zombie_pid>

# Signal parent to reap
$ kill -SIGCHLD <parent_pid>
```

## Monitoring Tools Summary

| Tool | Purpose | Install |
|------|---------|---------|
| `top` | Real-time process monitor | Built-in |
| `htop` | Better top | `apt install htop` |
| `atop` | Advanced system monitor | `apt install atop` |
| `iotop` | I/O usage by process | `apt install iotop` |
| `iftop` | Network usage | `apt install iftop` |
| `nethogs` | Network by process | `apt install nethogs` |

## Hands-On Exercise

1. Find processes by name:
   ```bash
   $ pgrep -a bash
   $ pidof bash
   ```

2. Start a process and stop it:
   ```bash
   $ sleep 300 &
   $ pgrep sleep
   $ kill %1
   $ jobs
   ```

3. Practice kill signals:
   ```bash
   $ sleep 1000 &
   $ kill -STOP $!           # Pause (! = last PID)
   $ jobs                    # Shows "Stopped"
   $ kill -CONT $!           # Resume
   $ kill $!                 # Terminate
   ```

4. Check what's using a port:
   ```bash
   $ sudo lsof -i :22
   $ sudo fuser -vn tcp 22
   ```

5. Find open files by a process:
   ```bash
   $ lsof -p $$              # Your current shell
   ```
