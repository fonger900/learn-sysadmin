---
title: 4. Core Protocols
order: 4
date: 2026-02-04
---
# Core Protocols

## TCP (Transmission Control Protocol)

TCP is a connection-oriented protocol that provides reliable, ordered, and error-checked delivery of data.

### Key Features
- **Reliability**: Guarantees delivery via acknowledgments and retransmissions
- **Ordering**: Data arrives in the correct order
- **Flow Control**: Prevents sender from overwhelming receiver (sliding window)
- **Congestion Control**: Avoids network overload (slow start, congestion avoidance)

### Three-Way Handshake
```
Client                    Server
   |                         |
   |-------- SYN ---------> |  (SEQ=100)
   |                         |
   |<----- SYN-ACK -------- |  (SEQ=300, ACK=101)
   |                         |
   |-------- ACK ---------> |  (SEQ=101, ACK=301)
   |                         |
   [   Connection Open   ]
```

### Four-Way Termination
```
Client                    Server
   |                         |
   |-------- FIN ---------> |
   |<------- ACK ---------- |
   |<------- FIN ---------- |
   |-------- ACK ---------> |
   |                         |
   [   Connection Closed   ]
```

### TCP Header (20 bytes minimum)
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Offs |Reserv | Flags         |            Window             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Common TCP Ports
| Port | Service |
|------|---------|
| 20/21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP |
| 80 | HTTP |
| 110 | POP3 |
| 143 | IMAP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |

---

## UDP (User Datagram Protocol)

UDP is a connectionless protocol that provides fast, best-effort delivery without guarantees.

### Key Features
- **No connection setup**: Send immediately
- **No reliability**: Packets may be lost, duplicated, or out of order
- **Low overhead**: 8-byte header vs TCP's 20+ bytes
- **Ideal for**: Real-time applications, streaming, DNS, gaming

### UDP Header (8 bytes)
```
 0      7 8     15 16    23 24    31
+--------+--------+--------+--------+
|   Source Port   |  Dest Port      |
+--------+--------+--------+--------+
|     Length      |   Checksum      |
+--------+--------+--------+--------+
```

### Common UDP Ports
| Port | Service |
|------|---------|
| 53 | DNS |
| 67/68 | DHCP |
| 69 | TFTP |
| 123 | NTP |
| 161/162 | SNMP |
| 514 | Syslog |

---

## DNS (Domain Name System)

DNS translates human-readable domain names to IP addresses.

### How DNS Resolution Works
```
1. User types "example.com"
2. Check local cache
3. Query recursive resolver (ISP or 8.8.8.8)
4. Resolver queries root server (.)
5. Root directs to .com TLD server
6. TLD directs to authoritative server for example.com
7. Authoritative server returns IP
8. Resolver caches and returns to user
```

### DNS Record Types
| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | example.com → 93.184.216.34 |
| AAAA | IPv6 address | example.com → 2606:2800:220:1:... |
| CNAME | Alias | www.example.com → example.com |
| MX | Mail server | example.com → mail.example.com |
| NS | Name server | example.com → ns1.example.com |
| TXT | Text data | SPF, DKIM, verification |
| PTR | Reverse lookup | 34.216.184.93 → example.com |
| SOA | Zone authority | Primary nameserver info |

### DNS Commands
```bash
# Forward lookup
$ dig example.com A
$ nslookup example.com

# Reverse lookup
$ dig -x 93.184.216.34

# Query specific server
$ dig @8.8.8.8 example.com

# Trace the resolution path
$ dig +trace example.com
```

---

## DHCP (Dynamic Host Configuration Protocol)

DHCP automatically assigns IP addresses and network configuration to devices.

### DORA Process
```
Client                    Server
   |                         |
   |------ DISCOVER ------> |  (Broadcast: "Anyone have an IP?")
   |                         |
   |<------ OFFER --------- |  ("Here's 192.168.1.10")
   |                         |
   |------ REQUEST -------> |  ("I'll take 192.168.1.10")
   |                         |
   |<---- ACKNOWLEDGE ----- |  ("It's yours for 24 hours")
```

### DHCP Provides
- IP address
- Subnet mask
- Default gateway
- DNS servers
- Lease time
- Domain name

### View DHCP Lease
```bash
# Linux
$ cat /var/lib/dhcp/dhclient.leases

# macOS
$ ipconfig getpacket en0

# Windows
> ipconfig /all
```

---

## HTTP/HTTPS

### HTTP (HyperText Transfer Protocol)
Application-layer protocol for web communication.

### Request Methods
| Method | Purpose | Idempotent |
|--------|---------|------------|
| GET | Retrieve | Yes |
| POST | Create | No |
| PUT | Update (full) | Yes |
| PATCH | Update (partial) | No |
| DELETE | Remove | Yes |
| HEAD | Headers only | Yes |
| OPTIONS | Allowed methods | Yes |

### HTTP Status Codes
| Code | Category | Example |
|------|----------|---------|
| 1xx | Informational | 100 Continue |
| 2xx | Success | 200 OK, 201 Created |
| 3xx | Redirect | 301 Moved, 304 Not Modified |
| 4xx | Client Error | 400 Bad Request, 404 Not Found |
| 5xx | Server Error | 500 Internal, 502 Bad Gateway |

### HTTPS
HTTP + TLS encryption. Uses port 443.

```bash
# Test HTTP headers
$ curl -I https://example.com

# View TLS certificate
$ openssl s_client -connect example.com:443
```

---

## Hands-On Exercises

### 1. Capture DNS Traffic
```bash
$ sudo tcpdump -i eth0 port 53 -n
```
Then in another terminal: `dig google.com`

### 2. Inspect a TCP Handshake
```bash
$ sudo tcpdump -i eth0 port 80 -n -c 10
```
Then: `curl http://example.com`

### 3. Test DHCP Renewal
```bash
$ sudo dhclient -r && sudo dhclient
```
