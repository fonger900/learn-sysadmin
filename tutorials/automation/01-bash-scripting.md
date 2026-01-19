---
title: 1. Bash Scripting
date: 2026-01-20
order: 1
---
# Bash Scripting

Automate repetitive tasks by putting commands into a file.

## The Shebang
Every script starts with `#!/bin/bash` to tell the system which interpreter to use.

## Basic Script
Create `hello.sh`:
```bash
#!/bin/bash
name="Alice"
echo "Hello, $name"
```

## Running Scripts
1. Make executable: `chmod +x hello.sh`
2. Run: `./hello.sh`

## Variables and Loops
```bash
#!/bin/bash
for i in {1..5}
do
   echo "Number: $i"
done
```
