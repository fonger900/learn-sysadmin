---
title: 2. The OSI Model
date: 2026-02-02
---
# The OSI Model

The Open Systems Interconnection (OSI) model describes seven layers that computer systems use to communicate over a network.

## The 7 Layers
1. **Physical**: Cables, fiber, wireless. (Bits)
2. **Data Link**: Switches, MAC addresses. (Frames)
3. **Network**: Routers, IP addresses. (Packets)
4. **Transport**: TCP/UDP, ports. (Segments)
5. **Session**: Session management.
6. **Presentation**: Encryption, data formatting.
7. **Application**: HTTP, FTP, DNS.

## Mnemonics
"**P**lease **D**o **N**ot **T**hrow **S**ausage **P**izza **A**way" (Bottom-up: Physical to Application).

## Encapsulation
As data moves down the stack, each layer adds a header (and sometimes a footer). This is called encapsulation.
