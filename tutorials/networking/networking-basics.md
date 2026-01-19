---
title: 1. Networking Basics
order: 1
date: 2026-02-01
---
# Networking Basics

## What is a Network?
A network is a collection of computers, servers, mainframes, network devices, peripherals, or other devices connected to one another to allow the sharing of data. The purpose of a network is to enable communication and resource sharing.

### Types of Networks by Scale
| Type | Range | Example |
|------|-------|---------|
| **PAN** (Personal Area Network) | ~10 meters | Bluetooth devices |
| **LAN** (Local Area Network) | Building/Campus | Office network |
| **MAN** (Metropolitan Area Network) | City | City-wide WiFi |
| **WAN** (Wide Area Network) | Global | The Internet |

## LAN vs WAN

### LAN (Local Area Network)
A LAN connects devices within a limited geographical area.

**Characteristics:**
- High speed (1 Gbps - 10 Gbps typical)
- Low latency
- Privately owned and managed
- Uses Ethernet (IEEE 802.3) or WiFi (IEEE 802.11)

**Common Topologies:**
- **Star**: All devices connect to a central switch (most common today)
- **Bus**: Single cable backbone (legacy)
- **Ring**: Devices form a closed loop (legacy, used in Token Ring)

### WAN (Wide Area Network)
A WAN spans large geographical distances, often connecting multiple LANs.

**Characteristics:**
- Lower speed than LAN (varies widely)
- Higher latency
- Often uses leased lines or internet connections
- Examples: MPLS, VPN over Internet, dedicated fiber

## Network Hardware

### Network Interface Card (NIC)
The hardware that connects a device to the network. Every NIC has a unique **MAC address** (e.g., `00:1A:2B:3C:4D:5E`).

### Switch
Connects devices within a single LAN. Operates at **Layer 2** (Data Link).

**How it works:**
1. Learns MAC addresses of connected devices
2. Builds a MAC address table
3. Forwards frames only to the correct port (unicast)
4. Floods unknown destinations to all ports

```
Device A ──┐
Device B ──┼── [SWITCH] ── Router ── Internet
Device C ──┘
```

### Router
Connects different networks together. Operates at **Layer 3** (Network).

**Key Functions:**
- Routes packets between networks using IP addresses
- Performs NAT (Network Address Translation)
- Acts as the default gateway for LAN devices
- Can implement firewall rules and QoS

### Access Point (AP)
Extends wired network to wireless clients. Operates at **Layer 2**.

### Firewall
Filters traffic based on rules. Can operate at Layer 3-7.

## Network Cables

### Ethernet Cables (Twisted Pair)
| Category | Speed | Distance |
|----------|-------|----------|
| Cat5e | 1 Gbps | 100m |
| Cat6 | 10 Gbps | 55m |
| Cat6a | 10 Gbps | 100m |
| Cat7 | 10 Gbps | 100m |
| Cat8 | 25-40 Gbps | 30m |

### Fiber Optic
- **Single-mode (SMF)**: Long distance (km), yellow jacket
- **Multi-mode (MMF)**: Short distance (hundreds of meters), orange/aqua jacket

## Hands-On Exercise
1. Open a terminal and run:
```bash
$ ip link show
# or on macOS:
$ ifconfig
```
2. Identify your network interfaces and their MAC addresses.
3. Find your default gateway:
```bash
$ ip route | grep default
# or on macOS:
$ netstat -rn | grep default
```
