---
title: 1. Viewing Processes
date: 2026-01-20
order: 1
---
# Understanding and Viewing Processes

Every running program on your Linux system is a process. Understanding how processes work is essential for system administration, troubleshooting, and performance tuning.

## What is a Process?

A process is an instance of a running program. Each process has:
- **PID**: Unique Process ID
- **PPID**: Parent Process ID
- **UID**: User ID of the owner
- **State**: Current execution state
- **Priority**: Scheduling priority
- **Resources**: CPU time, memory, open files

```bash
$ ps
    PID TTY          TIME CMD
   1234 pts/0    00:00:00 bash
   5678 pts/0    00:00:00 ps
```

## Process States

| State | Symbol | Description |
|-------|--------|-------------|
| Running | `R` | Currently executing or ready to run |
| Sleeping | `S` | Waiting for an event (interruptible) |
| Uninterruptible Sleep | `D` | Waiting for I/O (cannot be killed) |
| Stopped | `T` | Stopped by signal or debugger |
| Zombie | `Z` | Terminated but not reaped by parent |

### Process State Lifecycle
```
[ New ] → [ Ready ] ⇄ [ Running ] → [ Terminated ] → [ Zombie ]
              ↓             ↓
         [ Sleeping ] ← [ Waiting ]
```

A **zombie process** occurs when a child process terminates but the parent hasn't collected its exit status. They consume minimal resources but indicate poor programming.

## The `ps` Command

`ps` displays a snapshot of current processes.

### Common Options

| Command | Description |
|---------|-------------|
| `ps` | Processes in current terminal |
| `ps aux` | All processes, detailed format |
| `ps -ef` | All processes, full format |
| `ps -u username` | Processes by user |
| `ps -p 1234` | Specific PID |
| `ps --forest` | Show process tree |

### Understanding `ps aux` Output

```bash
$ ps aux | head -3
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 167840 13220 ?        Ss   Jan15   0:08 /sbin/init
root         2  0.0  0.0      0     0 ?        S    Jan15   0:00 [kthreadd]
```

| Column | Description |
|--------|-------------|
| USER | Process owner |
| PID | Process ID |
| %CPU | CPU usage percentage |
| %MEM | Memory usage percentage |
| VSZ | Virtual memory size (KB) |
| RSS | Resident set size - actual memory (KB) |
| TTY | Terminal (`?` = no terminal) |
| STAT | Process state |
| START | Start time |
| TIME | Total CPU time |
| COMMAND | Command that started the process |

### STAT Column Explained

| Symbol | Meaning |
|--------|---------|
| `S` | Sleeping |
| `R` | Running |
| `D` | Uninterruptible sleep |
| `Z` | Zombie |
| `T` | Stopped |
| `<` | High priority (nice < 0) |
| `N` | Low priority (nice > 0) |
| `s` | Session leader |
| `l` | Multi-threaded |
| `+` | Foreground process group |

## The `top` Command

`top` shows real-time process information and system statistics.

```bash
$ top
```

### Top Output Sections

**Header - System Overview:**
```
top - 14:30:52 up 10 days,  3:20,  2 users,  load average: 0.15, 0.10, 0.05
Tasks: 237 total,   1 running, 236 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.3 us,  0.7 sy,  0.0 ni, 96.8 id,  0.2 wa,  0.0 hi,  0.0 si
MiB Mem :  7851.5 total,  1234.5 free,  4567.0 used,  2050.0 buff/cache
MiB Swap:  2048.0 total,  2048.0 free,     0.0 used.  2901.5 avail Mem
```

| Metric | Description |
|--------|-------------|
| load average | 1, 5, 15 minute CPU load |
| us | User space CPU % |
| sy | Kernel space CPU % |
| id | Idle CPU % |
| wa | I/O wait % |

### Interactive Commands in Top

| Key | Action |
|-----|--------|
| `q` | Quit |
| `k` | Kill a process (enter PID) |
| `r` | Renice a process |
| `M` | Sort by memory |
| `P` | Sort by CPU |
| `u` | Filter by user |
| `1` | Show individual CPUs |
| `c` | Show full command path |
| `h` | Help |
| `?` | Help |

### Useful Top Variations
```bash
$ top -u username      # Show only user's processes
$ top -p 1234,5678     # Monitor specific PIDs
$ top -b -n 1          # Batch mode (for scripts)
```

## The `htop` Command

`htop` is a more user-friendly, colorful alternative (may need installation):

```bash
$ sudo apt install htop    # Debian/Ubuntu
$ sudo dnf install htop    # RHEL/Fedora
$ htop
```

**Features over top:**
- Colored display
- Scroll horizontally/vertically
- Mouse support
- Easy process filtering
- Kill without entering PID

## Process Priority and Nice Values

Every process has a priority that determines CPU scheduling.

| Concept | Range | Default | Description |
|---------|-------|---------|-------------|
| Nice | -20 to 19 | 0 | User-controlled priority |
| Priority | 0 to 139 | 80 | Actual kernel priority |

- **Lower nice = higher priority** (gets more CPU)
- Only root can set negative nice values

### Viewing Nice Values
```bash
$ ps -eo pid,ni,comm | head
$ top     # NI column
```

### Starting with Nice Value
```bash
$ nice -n 10 ./cpu_heavy_task.sh      # Lower priority
$ sudo nice -n -10 ./important.sh     # Higher priority (root)
```

### Changing Running Process Priority
```bash
$ renice 10 -p 1234         # Set PID 1234 to nice 10
$ renice -5 -p 1234         # Higher priority (root)
$ renice 15 -u username     # All processes by user
```

## Background Jobs

Run commands in the background to continue using the terminal.

### Running in Background
```bash
$ ./long_running_script.sh &          # Start in background
[1] 12345                              # [job number] PID

$ nohup ./script.sh &                  # Background + survives logout
$ nohup ./script.sh > output.log 2>&1 &   # With output redirect
```

### Job Control
```bash
$ jobs                    # List background jobs
$ jobs -l                 # List with PIDs

$ fg                      # Bring most recent job to foreground
$ fg %1                   # Bring job 1 to foreground

$ bg                      # Resume stopped job in background
$ bg %2                   # Resume job 2 in background
```

### Stopping and Resuming
```
Ctrl + Z    # Suspend (stop) current foreground job
Ctrl + C    # Terminate current foreground job
```

```bash
$ ./task.sh
^Z                        # Suspend
[1]+  Stopped    ./task.sh
$ bg                      # Resume in background
[1]+ ./task.sh &
```

## The `/proc` Filesystem

Linux exposes process information through `/proc`:

```bash
$ ls /proc/1234/          # Directory for PID 1234
cmdline  cwd  environ  exe  fd  maps  stat  status  ...

$ cat /proc/1234/cmdline  # Command line
$ cat /proc/1234/status   # Detailed status
$ ls -l /proc/1234/fd/    # Open file descriptors
$ readlink /proc/1234/cwd # Current working directory
```

### System Information in /proc
```bash
$ cat /proc/cpuinfo       # CPU information
$ cat /proc/meminfo       # Memory information
$ cat /proc/uptime        # System uptime
$ cat /proc/loadavg       # Load average
```

## Hands-On Exercise

1. View all running processes:
   ```bash
   $ ps aux | wc -l        # Count processes
   $ ps aux --sort=-%cpu | head  # Top CPU consumers
   ```

2. Monitor system with top:
   ```bash
   $ top
   # Press 'M' to sort by memory
   # Press 'P' to sort by CPU
   # Press 'q' to quit
   ```

3. Run a background job:
   ```bash
   $ sleep 300 &
   $ jobs
   $ fg
   # Press Ctrl+Z to suspend
   $ bg
   $ jobs
   ```

4. Check process details in /proc:
   ```bash
   $ echo $$                      # Your shell's PID
   $ cat /proc/$$/status | grep -E "Name|State|Pid"
   ```

5. Nice a process:
   ```bash
   $ nice -n 19 sleep 100 &
   $ ps -eo pid,ni,comm | grep sleep
   ```
