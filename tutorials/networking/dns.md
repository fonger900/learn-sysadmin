---
title: 5. DNS (Domain Name System)
order: 5
date: 2026-02-05
---
# DNS (Domain Name System)

DNS translates human-readable domain names to IP addresses. Understanding DNS is essential for troubleshooting network connectivity issues.

## How DNS Works

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

## DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| **A** | IPv4 address | `google.com -> 142.250.80.46` |
| **AAAA** | IPv6 address | `google.com -> 2607:f8b0:4004::...` |
| **CNAME** | Alias | `www.example.com -> example.com` |
| **MX** | Mail server | `example.com -> mail.example.com` |
| **NS** | Name server | `example.com -> ns1.example.com` |
| **TXT** | Text record | SPF, DKIM, verification |
| **PTR** | Reverse DNS | IP -> hostname |
| **SOA** | Start of Authority | Zone info, serial, TTL |

## DNS Configuration Files

### `/etc/hosts` - Local Name Resolution

First place Linux checks for name resolution:

```bash
$ cat /etc/hosts
127.0.0.1       localhost
127.0.1.1       myhostname
192.168.1.100   server1.local server1
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
```

| Directive | Description |
|-----------|-------------|
| `nameserver` | DNS server IP (max 3) |
| `search` | Domain search list |
| `domain` | Default domain |

### `/etc/nsswitch.conf` - Name Service Switch

Controls the order of name resolution:

```bash
$ grep hosts /etc/nsswitch.conf
hosts:          files dns
```

## DNS Query Tools

### `dig` - DNS Information Groper

```bash
# Basic query
$ dig google.com

# Query specific record type
$ dig google.com MX
$ dig google.com TXT

# Short answer only
$ dig +short google.com

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
```

## Common DNS Issues

### Troubleshooting Steps

1. **Check if DNS is the problem:**
   ```bash
   $ ping 8.8.8.8        # Works? Network is OK
   $ ping google.com     # Fails? DNS problem
   ```

2. **Check DNS configuration:**
   ```bash
   $ cat /etc/resolv.conf
   ```

3. **Test with different DNS server:**
   ```bash
   $ dig @8.8.8.8 example.com
   ```

4. **Check local hosts file:**
   ```bash
   $ grep example.com /etc/hosts
   ```

## Hands-On Exercise

1. Query DNS records:
   ```bash
   $ dig google.com +short
   $ dig google.com MX
   $ dig @8.8.8.8 google.com
   ```

2. Check your DNS configuration:
   ```bash
   $ cat /etc/resolv.conf
   $ cat /etc/hosts
   ```

3. Compare resolution methods:
   ```bash
   $ dig +short google.com
   $ getent hosts google.com
   ```

4. Trace DNS resolution:
   ```bash
   $ dig +trace google.com
   ```
