---
title: 1. IP Addressing and DNS
date: 2026-01-20
order: 1
---
# IP Addressing & DNS

Understanding IP addressing and DNS is fundamental for network troubleshooting and configuration.

## IP Addressing

Every device on a network needs a unique IP address to communicate.

### IPv4 Addresses

IPv4 uses 32-bit addresses written as four octets:
```
192.168.1.100
```

| Class | Range | Default Mask | Purpose |
|-------|-------|--------------|---------|
| A | 1.0.0.0 - 126.255.255.255 | /8 (255.0.0.0) | Large networks |
| B | 128.0.0.0 - 191.255.255.255 | /16 (255.255.0.0) | Medium networks |
| C | 192.0.0.0 - 223.255.255.255 | /24 (255.255.255.0) | Small networks |

### Private IP Ranges (RFC 1918)

These addresses are not routable on the internet:

| Class | Range | CIDR |
|-------|-------|------|
| A | 10.0.0.0 - 10.255.255.255 | 10.0.0.0/8 |
| B | 172.16.0.0 - 172.31.255.255 | 172.16.0.0/12 |
| C | 192.168.0.0 - 192.168.255.255 | 192.168.0.0/16 |

### Special Addresses

| Address | Purpose |
|---------|---------|
| 127.0.0.1 | Localhost (loopback) |
| 0.0.0.0 | All interfaces / default route |
| 255.255.255.255 | Broadcast |
| 169.254.x.x | Link-local (APIPA) - no DHCP |

### IPv6 Addresses

128-bit addresses, written in hexadecimal:
```
2001:0db8:85a3:0000:0000:8a2e:0370:7334
```

Shortened form (omit leading zeros, collapse `::`):
```
2001:db8:85a3::8a2e:370:7334
```

| Prefix | Type |
|--------|------|
| `::1` | Localhost |
| `fe80::/10` | Link-local |
| `2000::/3` | Global unicast |
| `fc00::/7` | Unique local (private) |

## Viewing Network Configuration

### `ip` Command (Modern)

```bash
# View IP addresses
$ ip addr
$ ip a                     # Short form

# View specific interface
$ ip addr show eth0

# View routing table
$ ip route
$ ip r                     # Short form

# View neighbors (ARP)
$ ip neigh
```

### `ifconfig` (Legacy)

```bash
$ ifconfig                 # All interfaces
$ ifconfig eth0            # Specific interface
```

### Practical Examples

```bash
# Get your IP address
$ ip addr show | grep "inet " | grep -v 127.0.0.1

# Get default gateway
$ ip route | grep default
default via 192.168.1.1 dev eth0

# Get your public IP
$ curl ifconfig.me
$ curl ipinfo.io/ip
```

## DNS (Domain Name System)

DNS translates human-readable domain names to IP addresses.

### How DNS Works

```
┌──────────────┐    ┌─────────────────┐    ┌──────────────────┐
│  Browser     │ -> │  Recursive DNS  │ -> │  Root Server     │
│  "google.com"│    │  (ISP/8.8.8.8)  │    │  "ask .com NS"   │
└──────────────┘    └─────────────────┘    └──────────────────┘
                           │                        │
                           ▼                        ▼
                    ┌──────────────────┐    ┌──────────────────┐
                    │  Cache result    │ <- │  .com TLD NS     │
                    │  142.250.x.x     │    │  "ask google NS" │
                    └──────────────────┘    └──────────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────────┐
                                            │  google.com NS   │
                                            │  "142.250.x.x"   │
                                            └──────────────────┘
```

### DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| **A** | IPv4 address | `google.com -> 142.250.80.46` |
| **AAAA** | IPv6 address | `google.com -> 2607:f8b0:4004::...` |
| **CNAME** | Alias | `www.example.com -> example.com` |
| **MX** | Mail server | `example.com -> mail.example.com` |
| **NS** | Name server | `example.com -> ns1.example.com` |
| **TXT** | Text record | SPF, DKIM, verification |
| **PTR** | Reverse DNS | `1.1.168.192.in-addr.arpa -> host.example.com` |
| **SOA** | Start of Authority | Zone info, serial, TTL |

## DNS Configuration Files

### `/etc/hosts` - Local Name Resolution

First place Linux checks for name resolution:

```bash
$ cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       myhostname
192.168.1.100   server1.local server1
192.168.1.101   database.local database
```

Use for:
- Development environments
- Blocking websites
- Local network hosts

### `/etc/resolv.conf` - DNS Server Configuration

Defines which DNS servers to query:

```bash
$ cat /etc/resolv.conf
nameserver 8.8.8.8
nameserver 8.8.4.4
search example.com local
options timeout:2 attempts:3
```

| Directive | Description |
|-----------|-------------|
| `nameserver` | DNS server IP (max 3) |
| `search` | Domain search list |
| `domain` | Default domain for incomplete names |
| `options` | Various options |

> **Note**: On modern systems, this file is often managed by `systemd-resolved` or `NetworkManager`.

### `/etc/nsswitch.conf` - Name Service Switch

Controls the order of name resolution:

```bash
$ grep hosts /etc/nsswitch.conf
hosts:          files dns
```

| Source | Description |
|--------|-------------|
| `files` | /etc/hosts |
| `dns` | DNS servers |
| `mdns` | Multicast DNS (Avahi) |

## DNS Query Tools

### `dig` - DNS Information Groper

```bash
# Basic query
$ dig google.com

# Query specific record type
$ dig google.com A
$ dig google.com MX
$ dig google.com TXT
$ dig google.com ANY

# Short answer only
$ dig +short google.com
142.250.80.46

# Specify DNS server
$ dig @8.8.8.8 google.com

# Trace full resolution path
$ dig +trace google.com

# Reverse lookup
$ dig -x 8.8.8.8
```

### `nslookup` - Name Server Lookup

```bash
# Basic query
$ nslookup google.com

# Specify DNS server
$ nslookup google.com 8.8.8.8

# Query specific type
$ nslookup -type=mx google.com
```

### `host` - Simple DNS Lookup

```bash
$ host google.com
$ host -t mx google.com
$ host 8.8.8.8              # Reverse lookup
```

### `getent` - Get Entries

```bash
# Query using system settings (follows nsswitch.conf)
$ getent hosts google.com
$ getent ahosts google.com   # All addresses
```

## Network Connectivity Testing

### `ping` - Test Reachability

```bash
$ ping google.com           # Continuous ping
$ ping -c 4 google.com      # 4 pings only
$ ping -i 0.5 google.com    # 0.5 second interval
$ ping6 google.com          # IPv6
```

### `traceroute` - Trace Network Path

```bash
$ traceroute google.com
$ traceroute -n google.com  # No DNS lookup
$ mtr google.com            # Interactive traceroute
```

## Configuring Static IP

### Temporary (until reboot)

```bash
# Add IP address
$ sudo ip addr add 192.168.1.100/24 dev eth0

# Set default gateway
$ sudo ip route add default via 192.168.1.1

# Delete IP
$ sudo ip addr del 192.168.1.100/24 dev eth0
```

### Permanent (Netplan - Ubuntu)

`/etc/netplan/01-netcfg.yaml`:
```yaml
network:
  version: 2
  ethernets:
    eth0:
      addresses:
        - 192.168.1.100/24
      gateway4: 192.168.1.1
      nameservers:
        addresses:
          - 8.8.8.8
          - 8.8.4.4
```

```bash
$ sudo netplan apply
```

### Permanent (NetworkManager - RHEL/Fedora)

```bash
$ sudo nmcli con mod "Wired connection 1" \
    ipv4.addresses 192.168.1.100/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "8.8.8.8 8.8.4.4" \
    ipv4.method manual
$ sudo nmcli con up "Wired connection 1"
```

## Hands-On Exercise

1. View your network configuration:
   ```bash
   $ ip addr
   $ ip route
   $ cat /etc/resolv.conf
   ```

2. Test DNS resolution:
   ```bash
   $ dig google.com +short
   $ dig @8.8.8.8 google.com
   $ host google.com
   ```

3. Check /etc/hosts:
   ```bash
   $ cat /etc/hosts
   $ ping localhost
   ```

4. Test network connectivity:
   ```bash
   $ ping -c 4 8.8.8.8        # By IP (no DNS)
   $ ping -c 4 google.com     # By name (uses DNS)
   ```

5. Trace network path:
   ```bash
   $ traceroute -n google.com
   ```
