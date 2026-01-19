---
title: 5. Network Diagnostic Tools
date: 2026-02-05
---
# Network Diagnostic Tools

## `ping`
Tests reachability to a host using ICMP Echo Requests.
```bash
$ ping google.com
```

## `traceroute`
Shows the path (hops) packets take to reach a destination.
```bash
$ traceroute google.com
```

## `netstat` / `ss`
Displays network connections, routing tables, and interface statistics. `ss` is the modern replacement.
```bash
$ ss -tunl
# -t: tcp, -u: udp, -n: numeric, -l: listening
```

## `nmap`
Network exploration tool and security scanner.
```bash
$ nmap -sP 192.168.1.0/24
```
