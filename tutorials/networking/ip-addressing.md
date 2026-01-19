---
title: 3. IP Addressing and Subnetting
order: 3
date: 2026-02-03
---
# IP Addressing and Subnetting

## IPv4 Fundamentals

### Structure
An IPv4 address is a 32-bit number, typically written as four octets in decimal (dotted-decimal notation).

```
192.168.1.100
 │   │   │  │
 │   │   │  └─ Host portion
 │   │   └──── Network portion
 │   └──────── (depends on subnet mask)
 └────────────
```

### Binary Representation
```
192     .  168    .   1     .  100
11000000.10101000.00000001.01100100
```

Each octet = 8 bits, so 4 octets = 32 bits.

---

## Subnet Masks

A subnet mask determines which portion of an IP address is the network and which is the host.

### Common Subnet Masks
| CIDR | Subnet Mask | Hosts per Subnet |
|------|-------------|------------------|
| /8 | 255.0.0.0 | 16,777,214 |
| /16 | 255.255.0.0 | 65,534 |
| /24 | 255.255.255.0 | 254 |
| /25 | 255.255.255.128 | 126 |
| /26 | 255.255.255.192 | 62 |
| /27 | 255.255.255.224 | 30 |
| /28 | 255.255.255.240 | 14 |
| /29 | 255.255.255.248 | 6 |
| /30 | 255.255.255.252 | 2 |
| /32 | 255.255.255.255 | 1 (host route) |

**Note:** Usable hosts = 2^(32-CIDR) - 2 (network address and broadcast address are reserved)

---

## CIDR Notation

CIDR (Classless Inter-Domain Routing) replaced the old classful addressing system.

**Example:** `192.168.1.0/24`
- Network: `192.168.1.0`
- Subnet Mask: `255.255.255.0`
- Host Range: `192.168.1.1` to `192.168.1.254`
- Broadcast: `192.168.1.255`

---

## Private vs Public IP Addresses

### Private IP Ranges (RFC 1918)
These addresses are not routable on the public internet.

| Class | Range | CIDR | Typical Use |
|-------|-------|------|-------------|
| A | 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 | Large enterprises |
| B | 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 | Medium organizations |
| C | 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 | Home/small office |

### Special Addresses
| Address | Purpose |
|---------|---------|
| 127.0.0.0/8 | Loopback (localhost) |
| 169.254.0.0/16 | Link-local (APIPA) |
| 0.0.0.0/0 | Default route |
| 255.255.255.255 | Broadcast |

---

## Subnetting Practice

### Problem: Subnet 192.168.10.0/24 into 4 equal subnets.

**Solution:**
- Original: /24 = 256 addresses
- Need 4 subnets: 2^2 = 4, so borrow 2 bits → /26
- Each /26 = 64 addresses (62 usable)

| Subnet | Network | First Host | Last Host | Broadcast |
|--------|---------|------------|-----------|-----------|
| 1 | 192.168.10.0 | 192.168.10.1 | 192.168.10.62 | 192.168.10.63 |
| 2 | 192.168.10.64 | 192.168.10.65 | 192.168.10.126 | 192.168.10.127 |
| 3 | 192.168.10.128 | 192.168.10.129 | 192.168.10.190 | 192.168.10.191 |
| 4 | 192.168.10.192 | 192.168.10.193 | 192.168.10.254 | 192.168.10.255 |

---

## IPv6 Overview

IPv6 uses 128-bit addresses (vs IPv4's 32-bit), providing ~340 undecillion addresses.

### Format
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

**Rules for shortening:**
1. Leading zeros in each group can be omitted: `2001:db8:85a3:0:0:8a2e:370:7334`
2. One group of consecutive zeros can be replaced with `::`: `2001:db8:85a3::8a2e:370:7334`

### Special IPv6 Addresses
| Address | Purpose |
|---------|---------|
| ::1/128 | Loopback |
| ::/0 | Default route |
| fe80::/10 | Link-local |
| 2000::/3 | Global unicast |

---

## NAT (Network Address Translation)

NAT allows multiple devices on a private network to share a single public IP address.

### Types
- **SNAT (Source NAT)**: Translates source IP (typical home router)
- **DNAT (Destination NAT)**: Translates destination IP (port forwarding)
- **PAT (Port Address Translation)**: Maps ports to differentiate internal hosts

### How It Works
```
[192.168.1.10:12345] → [Router NAT] → [203.0.113.5:54321] → Internet
```

---

## Hands-On Exercises

### 1. View Your IP Configuration
```bash
$ ip addr show
# or on macOS:
$ ifconfig
```

### 2. Calculate a Subnet
Given: `10.50.100.0/22`
- How many usable hosts?
- What is the broadcast address?
- What is the valid host range?

**Answer:**
- Usable hosts: 2^(32-22) - 2 = 1022
- Network: 10.50.100.0
- Broadcast: 10.50.103.255
- Range: 10.50.100.1 - 10.50.103.254

### 3. Use `ipcalc` (install if needed)
```bash
$ ipcalc 192.168.1.0/24
```
