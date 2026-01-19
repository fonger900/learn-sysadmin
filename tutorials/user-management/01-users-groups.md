---
title: 1. Users and Groups
date: 2026-01-20
order: 1
---
# Users and Groups

## Concepts
- **User**: An entity that can log in or own files. Identified by UID (User ID).
- **Group**: A collection of users. Identified by GID (Group ID).

## Managing Users
- `useradd username`: Create a new user
- `passwd username`: Set usage password
- `usermod`: Modify user account
- `userdel username`: Delete user

## Managing Groups
- `groupadd groupname`: Create a new group
- `usermod -aG groupname username`: Add user to a group
- `groups username`: Show groups a user belongs to

## Important Files
- `/etc/passwd`: Stores user information
- `/etc/group`: Stores group information
- `/etc/shadow`: Stores encrypted passwords (restricted access)
