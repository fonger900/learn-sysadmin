---
title: 2. Managing Processes
date: 2026-01-20
order: 2
---
# Managing Processes

Sometimes processes misbehave or need to be stopped.

## Signals
You control processes by sending signals.
- `SIGTERM` (15): Polite request to terminate (default).
- `SIGKILL` (9): Force kill immediately.

## The `kill` Command
- `kill PID`: Send SIGTERM to Process ID (PID).
- `kill -9 PID`: Send SIGKILL to PID.

## The `killall` Command
- `killall firefox`: Kill all processes with name "firefox".
