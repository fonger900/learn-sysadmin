---
title: 5. Network Diagnostic Tools
order: 5
date: 2026-02-05
---
# Network Diagnostic Tools

## ping

Tests reachability to a host using ICMP Echo Requests.

### Basic Usage
```bash
$ ping google.com
PING google.com (142.250.190.46): 56 data bytes
64 bytes from 142.250.190.46: icmp_seq=0 ttl=117 time=12.3 ms
64 bytes from 142.250.190.46: icmp_seq=1 ttl=117 time=11.8 ms
```

### Options
```bash
# Limit count
$ ping -c 5 google.com

# Set interval (seconds)
$ ping -i 0.2 google.com

# Set packet size
$ ping -s 1000 google.com

# Flood ping (requires root, be careful!)
$ sudo ping -f google.com
```

### Understanding Output
- **icmp_seq**: Sequence number (detect packet loss)
- **ttl**: Time To Live (hops remaining)
- **time**: Round-trip time in milliseconds

### Troubleshooting
| Result | Meaning |
|--------|---------|
| Reply received | Host reachable |
| Request timeout | Host unreachable or blocking ICMP |
| Destination unreachable | No route to host |
| TTL expired | Too many hops |

---

## traceroute / tracepath

Shows the path (hops) packets take to reach a destination.

### Basic Usage
```bash
# Linux
$ traceroute google.com

# macOS
$ traceroute google.com

# Windows
> tracert google.com
```

### Sample Output
```
traceroute to google.com (142.250.190.46), 30 hops max
 1  router.local (192.168.1.1)  1.234 ms
 2  isp-gateway.example.com (10.0.0.1)  8.567 ms
 3  core-router.isp.com (203.0.113.1)  15.890 ms
 4  * * *  (no response)
 5  google-edge.net (142.250.190.46)  12.345 ms
```

### Reading the Output
- Each line = one hop (router)
- `* * *` = No response (firewall or timeout)
- Three time measurements per hop

### Advanced Options
```bash
# Use ICMP instead of UDP (some firewalls block UDP)
$ sudo traceroute -I google.com

# Use TCP SYN
$ sudo traceroute -T -p 443 google.com

# Show AS numbers
$ traceroute -A google.com
```

---

## netstat / ss

Displays network connections, routing tables, and interface statistics.

### ss (Modern replacement for netstat)
```bash
# List all listening TCP ports
$ ss -tln

# List all listening UDP ports
$ ss -uln

# List all established connections
$ ss -t state established

# Show process using port
$ ss -tlnp

# Filter by port
$ ss -tln sport = :22
$ ss -tln dport = :443
```

### Common Options
| Option | Meaning |
|--------|---------|
| -t | TCP |
| -u | UDP |
| -l | Listening |
| -n | Numeric (no DNS resolution) |
| -p | Show process |
| -a | All sockets |
| -s | Summary statistics |

### netstat (Legacy)
```bash
$ netstat -an | grep LISTEN
$ netstat -rn  # Routing table
$ netstat -i   # Interface statistics
```

---

## nmap

Network exploration tool and security scanner.

### Host Discovery
```bash
# Ping scan (find live hosts)
$ nmap -sn 192.168.1.0/24

# No ping, just scan
$ nmap -Pn 192.168.1.1
```

### Port Scanning
```bash
# Scan common ports
$ nmap 192.168.1.1

# Scan specific ports
$ nmap -p 22,80,443 192.168.1.1

# Scan all 65535 ports
$ nmap -p- 192.168.1.1

# Fast scan (top 100 ports)
$ nmap -F 192.168.1.1
```

### Scan Types
```bash
# TCP SYN scan (default, requires root)
$ sudo nmap -sS 192.168.1.1

# TCP connect scan (no root needed)
$ nmap -sT 192.168.1.1

# UDP scan
$ sudo nmap -sU 192.168.1.1

# Combined TCP + UDP
$ sudo nmap -sSU 192.168.1.1
```

### Service/Version Detection
```bash
# Detect service versions
$ nmap -sV 192.168.1.1

# OS detection
$ sudo nmap -O 192.168.1.1

# Aggressive scan (version, OS, scripts, traceroute)
$ sudo nmap -A 192.168.1.1
```

### Nmap Scripting Engine (NSE)
```bash
# Run default scripts
$ nmap -sC 192.168.1.1

# Run specific script
$ nmap --script=http-title 192.168.1.1

# List available scripts
$ ls /usr/share/nmap/scripts/
```

### Output Formats
```bash
# Normal text
$ nmap -oN scan.txt 192.168.1.1

# XML
$ nmap -oX scan.xml 192.168.1.1

# Grepable
$ nmap -oG scan.gnmap 192.168.1.1

# All formats
$ nmap -oA scan 192.168.1.1
```

---

## tcpdump

Command-line packet analyzer.

### Basic Capture
```bash
# Capture on interface
$ sudo tcpdump -i eth0

# Limit to 10 packets
$ sudo tcpdump -i eth0 -c 10

# Save to file
$ sudo tcpdump -i eth0 -w capture.pcap

# Read from file
$ tcpdump -r capture.pcap
```

### Filters
```bash
# By host
$ sudo tcpdump host 192.168.1.1

# By port
$ sudo tcpdump port 80

# By protocol
$ sudo tcpdump icmp
$ sudo tcpdump tcp
$ sudo tcpdump udp

# Complex filters
$ sudo tcpdump 'tcp port 80 and host 192.168.1.1'
$ sudo tcpdump 'src port 443'
$ sudo tcpdump 'dst net 10.0.0.0/8'
```

### Display Options
```bash
# Don't resolve hostnames
$ sudo tcpdump -n

# Show verbose output
$ sudo tcpdump -v

# Show hex dump
$ sudo tcpdump -X

# Show ASCII + hex
$ sudo tcpdump -XX
```

---

## curl

Transfer data with URLs (great for HTTP testing).

### Basic Requests
```bash
# GET request
$ curl https://example.com

# Show headers only
$ curl -I https://example.com

# Show headers + body
$ curl -i https://example.com

# Verbose (see handshake)
$ curl -v https://example.com
```

### HTTP Methods
```bash
# POST with data
$ curl -X POST -d "name=value" https://api.example.com/endpoint

# POST JSON
$ curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' \
  https://api.example.com/endpoint

# PUT
$ curl -X PUT -d @file.json https://api.example.com/resource

# DELETE
$ curl -X DELETE https://api.example.com/resource/1
```

### Useful Options
```bash
# Follow redirects
$ curl -L https://example.com

# Download file
$ curl -O https://example.com/file.zip

# Custom headers
$ curl -H "Authorization: Bearer TOKEN" https://api.example.com

# Silent mode
$ curl -s https://example.com

# Timeout
$ curl --connect-timeout 5 --max-time 10 https://example.com
```

---

## dig

DNS lookup utility.

### Basic Queries
```bash
# A record
$ dig example.com

# Specific record type
$ dig example.com MX
$ dig example.com NS
$ dig example.com TXT

# Short answer
$ dig +short example.com

# Reverse lookup
$ dig -x 93.184.216.34
```

### Advanced
```bash
# Query specific server
$ dig @8.8.8.8 example.com

# Trace resolution
$ dig +trace example.com

# TCP instead of UDP
$ dig +tcp example.com

# Show all records
$ dig example.com ANY
```

---

## Hands-On Lab

### Scenario: Troubleshoot connectivity to a web server

1. **Check if host is reachable:**
   ```bash
   $ ping -c 3 webserver.example.com
   ```

2. **Trace the path:**
   ```bash
   $ traceroute webserver.example.com
   ```

3. **Verify DNS resolution:**
   ```bash
   $ dig webserver.example.com
   ```

4. **Check if port 443 is open:**
   ```bash
   $ nmap -p 443 webserver.example.com
   ```

5. **Test HTTP response:**
   ```bash
   $ curl -I https://webserver.example.com
   ```

6. **Capture traffic for deeper analysis:**
   ```bash
   $ sudo tcpdump -i eth0 host webserver.example.com -w debug.pcap
   ```
