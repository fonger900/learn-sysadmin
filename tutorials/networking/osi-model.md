---
title: 2. The OSI Model
date: 2026-02-02
---
# The OSI Model

The Open Systems Interconnection (OSI) model is a conceptual framework that standardizes the functions of a communication system into seven distinct layers.

## Why Learn the OSI Model?
- **Troubleshooting**: Isolate problems by layer
- **Communication**: Common language for network professionals
- **Design**: Build modular, interoperable systems

## The 7 Layers (Bottom to Top)

### Layer 1: Physical
**Purpose**: Transmit raw bits over a physical medium.

**Components:**
- Cables (copper, fiber, coaxial)
- Hubs, repeaters
- Connectors (RJ45, LC, SC)
- Signal encoding (voltage levels, light pulses)

**Troubleshooting:** Check cables, verify link lights, test with cable tester.

---

### Layer 2: Data Link
**Purpose**: Reliable transfer of frames between adjacent nodes.

**Key Concepts:**
- **MAC Addresses**: 48-bit hardware addresses (e.g., `AA:BB:CC:DD:EE:FF`)
- **Frames**: Data unit at this layer
- **Switches**: Forward frames based on MAC address table
- **VLANs**: Logical segmentation of a physical network
- **ARP**: Maps IP addresses to MAC addresses

**Protocols:** Ethernet (802.3), WiFi (802.11), PPP

**Troubleshooting:** Check switch port status, verify VLAN membership, examine ARP table.
```bash
$ arp -a
$ ip neigh show
```

---

### Layer 3: Network
**Purpose**: Routing packets across different networks.

**Key Concepts:**
- **IP Addresses**: Logical addressing (IPv4/IPv6)
- **Packets**: Data unit at this layer
- **Routers**: Forward packets based on IP routing tables
- **Subnetting**: Dividing networks into smaller segments

**Protocols:** IP, ICMP, OSPF, BGP

**Troubleshooting:** Check IP configuration, verify routes, test with ping.
```bash
$ ip addr show
$ ip route show
$ ping 8.8.8.8
```

---

### Layer 4: Transport
**Purpose**: End-to-end communication, reliability, and flow control.

**Key Concepts:**
- **Ports**: Identify applications (e.g., HTTP=80, SSH=22)
- **Segments**: Data unit at this layer
- **TCP**: Connection-oriented, reliable, ordered delivery
- **UDP**: Connectionless, fast, no guaranteed delivery

**TCP Three-Way Handshake:**
```
Client           Server
   |--- SYN --->|
   |<-- SYN-ACK-|
   |--- ACK --->|
   [Connection Established]
```

**Troubleshooting:** Check port availability, verify firewall rules.
```bash
$ ss -tunl
$ netstat -an | grep LISTEN
```

---

### Layer 5: Session
**Purpose**: Manage sessions between applications.

**Key Concepts:**
- Session establishment, maintenance, termination
- Synchronization and checkpointing
- Examples: NetBIOS, RPC, SQL sessions

---

### Layer 6: Presentation
**Purpose**: Data translation, encryption, compression.

**Key Concepts:**
- Character encoding (ASCII, Unicode)
- Data encryption (TLS/SSL)
- Data compression (gzip)
- Format translation (JPEG, MPEG)

---

### Layer 7: Application
**Purpose**: Interface between network and user applications.

**Protocols:** HTTP, HTTPS, FTP, SMTP, DNS, SSH, DHCP

**Troubleshooting:** Check application logs, verify DNS resolution.
```bash
$ curl -I https://example.com
$ dig example.com
$ nslookup example.com
```

---

## OSI vs TCP/IP Model
| OSI Model | TCP/IP Model |
|-----------|--------------|
| Application | Application |
| Presentation | Application |
| Session | Application |
| Transport | Transport |
| Network | Internet |
| Data Link | Network Access |
| Physical | Network Access |

## Encapsulation
As data flows down the stack, each layer adds its header (and sometimes trailer).

```
Application Data
    ↓
[Transport Header | Data] = Segment
    ↓
[Network Header | Segment] = Packet
    ↓
[Frame Header | Packet | Frame Trailer] = Frame
    ↓
[Physical: Bits transmitted]
```

## Memory Tricks
**Top-down (Layer 7 to 1):**
"**A**ll **P**eople **S**eem **T**o **N**eed **D**ata **P**rocessing"

**Bottom-up (Layer 1 to 7):**
"**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way"

## Hands-On Exercise
Use `tcpdump` or Wireshark to capture packets and identify layers:
```bash
$ sudo tcpdump -i eth0 -c 10
```
