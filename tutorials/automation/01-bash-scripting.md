---
title: 1. Bash Scripting
date: 2026-01-20
order: 1
---
# Bash Scripting

Bash scripts automate repetitive tasks by putting commands into a file. Learning to script is essential for system administration.

## Your First Script

### Create the Script

```bash
$ vim hello.sh
```

```bash
#!/bin/bash
# My first script

echo "Hello, World!"
echo "Today is $(date)"
```

### Run the Script

```bash
$ chmod +x hello.sh       # Make executable
$ ./hello.sh              # Run it
Hello, World!
Today is Mon Jan 15 10:30:00 UTC 2024
```

## The Shebang

The first line tells the system which interpreter to use:

| Shebang | Interpreter |
|---------|-------------|
| `#!/bin/bash` | Bash shell |
| `#!/bin/sh` | POSIX shell |
| `#!/usr/bin/env bash` | Bash (portable) |
| `#!/usr/bin/env python3` | Python 3 |

## Variables

### Defining Variables

```bash
#!/bin/bash

# No spaces around the =
name="Alice"
age=25
today=$(date +%Y-%m-%d)

echo "Hello, $name"
echo "You are $age years old"
echo "Today is $today"
```

### Using Variables

| Syntax | Description |
|--------|-------------|
| `$var` | Variable value |
| `${var}` | Same, but clearer |
| `${var:-default}` | Use default if var is empty |
| `${var:=default}` | Set and use default if empty |
| `${#var}` | Length of var |

```bash
name="Alice"
echo "Hello ${name}!"
echo "Name length: ${#name}"    # 5

unset name
echo "Hello ${name:-Anonymous}" # Hello Anonymous
```

### Command Substitution

```bash
# Using $()
current_dir=$(pwd)
file_count=$(ls | wc -l)

# Using backticks (older style)
current_dir=`pwd`
```

### Environment Variables

```bash
echo "Home: $HOME"
echo "User: $USER"
echo "Path: $PATH"
echo "Shell: $SHELL"

# Export for child processes
export MY_VAR="value"
```

## Input and Arguments

### Command-Line Arguments

| Variable | Description |
|----------|-------------|
| `$0` | Script name |
| `$1`, `$2`, ... | First, second, ... argument |
| `$#` | Number of arguments |
| `$@` | All arguments (as separate words) |
| `$*` | All arguments (as single string) |

```bash
#!/bin/bash
echo "Script: $0"
echo "First arg: $1"
echo "Second arg: $2"
echo "Total args: $#"
echo "All args: $@"
```

```bash
$ ./script.sh hello world
Script: ./script.sh
First arg: hello
Second arg: world
Total args: 2
All args: hello world
```

### Reading User Input

```bash
#!/bin/bash

echo -n "Enter your name: "
read name
echo "Hello, $name!"

# With prompt
read -p "Enter your age: " age
echo "You are $age years old"

# Silent input (for passwords)
read -sp "Password: " password
echo  # New line
```

## Conditionals

### If Statements

```bash
#!/bin/bash

if [ "$1" = "hello" ]; then
    echo "Hello to you too!"
elif [ "$1" = "bye" ]; then
    echo "Goodbye!"
else
    echo "Unknown command"
fi
```

### Test Operators

**String comparisons:**
| Operator | Description |
|----------|-------------|
| `=` or `==` | Equal |
| `!=` | Not equal |
| `-z "$str"` | String is empty |
| `-n "$str"` | String is not empty |

**Numeric comparisons:**
| Operator | Description |
|----------|-------------|
| `-eq` | Equal |
| `-ne` | Not equal |
| `-lt` | Less than |
| `-le` | Less or equal |
| `-gt` | Greater than |
| `-ge` | Greater or equal |

**File tests:**
| Operator | Description |
|----------|-------------|
| `-e file` | File exists |
| `-f file` | Is a regular file |
| `-d file` | Is a directory |
| `-r file` | Is readable |
| `-w file` | Is writable |
| `-x file` | Is executable |
| `-s file` | File size > 0 |

```bash
#!/bin/bash

if [ -f "/etc/passwd" ]; then
    echo "File exists"
fi

if [ -d "/home" ]; then
    echo "Directory exists"
fi

if [ $# -lt 1 ]; then
    echo "Usage: $0 <filename>"
    exit 1
fi
```

### Double Brackets [[ ]]

More powerful than single brackets:

```bash
# Pattern matching
if [[ "$filename" == *.txt ]]; then
    echo "Text file"
fi

# Regex matching
if [[ "$email" =~ ^[a-z]+@[a-z]+\.[a-z]+$ ]]; then
    echo "Valid email"
fi

# Logical operators
if [[ -f "$file" && -r "$file" ]]; then
    echo "File exists and is readable"
fi
```

### Case Statements

```bash
#!/bin/bash

case "$1" in
    start)
        echo "Starting..."
        ;;
    stop)
        echo "Stopping..."
        ;;
    restart)
        echo "Restarting..."
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
```

## Loops

### For Loop

```bash
# Loop over list
for name in Alice Bob Carol; do
    echo "Hello, $name"
done

# Loop over range
for i in {1..5}; do
    echo "Number: $i"
done

# C-style for loop
for ((i=1; i<=5; i++)); do
    echo "Count: $i"
done

# Loop over files
for file in *.txt; do
    echo "Processing: $file"
done

# Loop over command output
for user in $(cut -d: -f1 /etc/passwd | head -5); do
    echo "User: $user"
done
```

### While Loop

```bash
#!/bin/bash

count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    ((count++))
done

# Read file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < /etc/passwd
```

### Until Loop

```bash
count=1
until [ $count -gt 5 ]; do
    echo "Count: $count"
    ((count++))
done
```

### Loop Control

```bash
# break - exit loop
for i in {1..10}; do
    if [ $i -eq 5 ]; then
        break
    fi
    echo $i
done

# continue - skip iteration
for i in {1..5}; do
    if [ $i -eq 3 ]; then
        continue
    fi
    echo $i
done
```

## Functions

```bash
#!/bin/bash

# Define function
greet() {
    local name=$1         # Local variable
    echo "Hello, $name!"
}

# With return value
add_numbers() {
    local result=$(( $1 + $2 ))
    echo $result          # "Return" via stdout
}

# Call functions
greet "Alice"
sum=$(add_numbers 5 3)
echo "Sum: $sum"
```

### Function Best Practices

```bash
#!/bin/bash

# Error handling function
die() {
    echo "ERROR: $1" >&2
    exit 1
}

# Usage
[ -f "$1" ] || die "File not found: $1"
```

## Input/Output Redirection

| Operator | Description |
|----------|-------------|
| `>` | Redirect stdout (overwrite) |
| `>>` | Redirect stdout (append) |
| `2>` | Redirect stderr |
| `2>&1` | Redirect stderr to stdout |
| `&>` | Redirect both stdout and stderr |
| `<` | Redirect stdin |
| `\|` | Pipe stdout to next command |

```bash
# Output to file
echo "Hello" > output.txt
echo "World" >> output.txt

# Error to file
command 2> errors.log

# Both to file
command &> all.log
command > all.log 2>&1

# Discard output
command > /dev/null 2>&1

# Read from file
while read line; do
    echo "$line"
done < input.txt
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Misuse of command |
| `126` | Permission denied |
| `127` | Command not found |

```bash
#!/bin/bash

if [ ! -f "$1" ]; then
    echo "File not found" >&2
    exit 1
fi

# Check previous command
if command; then
    echo "Success"
else
    echo "Failed with code: $?"
fi
```

## Practical Script Examples

### Backup Script

```bash
#!/bin/bash
set -e  # Exit on error

BACKUP_DIR="/backup"
SOURCE_DIR="/home"
DATE=$(date +%Y%m%d)
BACKUP_FILE="${BACKUP_DIR}/home_${DATE}.tar.gz"

# Create backup
echo "Creating backup..."
tar -czf "$BACKUP_FILE" "$SOURCE_DIR"

# Keep only last 7 backups
echo "Cleaning old backups..."
ls -t "${BACKUP_DIR}"/home_*.tar.gz | tail -n +8 | xargs -r rm

echo "Backup complete: $BACKUP_FILE"
```

### Log Monitoring Script

```bash
#!/bin/bash

LOG_FILE="/var/log/syslog"
PATTERN="error|fail|critical"

echo "Monitoring $LOG_FILE for: $PATTERN"
tail -f "$LOG_FILE" | grep -iE --line-buffered "$PATTERN"
```

## Hands-On Exercise

1. Create a greeting script:
   ```bash
   #!/bin/bash
   read -p "Enter your name: " name
   echo "Hello, ${name:-Guest}!"
   ```

2. Create a file checker:
   ```bash
   #!/bin/bash
   if [ -f "$1" ]; then
       echo "File: $1"
       echo "Lines: $(wc -l < "$1")"
   else
       echo "Not a file: $1"
   fi
   ```

3. Create a directory backup script:
   ```bash
   #!/bin/bash
   dir=${1:-.}
   tar -czf "backup_$(date +%Y%m%d).tar.gz" "$dir"
   ```

4. Practice loops:
   ```bash
   #!/bin/bash
   for f in *.txt; do
       [ -e "$f" ] || continue
       echo "Found: $f"
   done
   ```
