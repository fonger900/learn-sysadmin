---
title: 3. IP Addressing and Subnetting
date: 2026-02-03
---
# IP Addressing and Subnetting

## IPv4 Structure
An IPv4 address is a 32-bit number usually represented as four decimals separated by dots (e.g., `192.168.1.1`).

## Subnet Masks & CIDR
A subnet mask divides an IP address into network and host portions.
- **Class C**: `255.255.255.0`
- **CIDR (Classless Inter-Domain Routing)**: `/24` (meaning first 24 bits are network).

## Private IP Ranges (RFC 1918)
These addresses are not routable on the public internet.
- `10.0.0.0/8`
- `172.16.0.0/12`
- `192.168.0.0/16`

## Public IP
Your ISP assigns this. It identifies you to the rest of the world.
