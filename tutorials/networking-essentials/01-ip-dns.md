---
title: 1. IP Addressing and DNS
date: 2026-01-20
order: 1
---
# IP Addressing & DNS

## IP Addresses
Every device on a network needs an IP address.
- **IPv4**: `192.168.1.1`
- **IPv6**: `2001:db8::1`

## Commands
- `ip addr`: Show IP addresses
- `ping google.com`: Check connectivity
- `ip route`: Show routing table

## DNS (Domain Name System)
Translates names (google.com) to IPs (142.250.x.x).
- `nslookup google.com`: Query DNS
- `dig google.com`: Detailed DNS query
- `/etc/resolv.conf`: DNS server configuration
