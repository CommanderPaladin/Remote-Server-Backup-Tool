# Remote Server Backup and Synchronization Script

## Script Name

`remote_server_backup_sync.py`

## Overview

This script facilitates the backup and synchronization of data from a remote server to a local machine. It includes an option to create a backup of MongoDB databases on the remote server before syncing the entire file system. The synchronization process utilizes `rsync` to ensure reliable and resumable file transfers. Users also have the option to skip the MongoDB backup step if desired.

## Features

- Backup MongoDB data from a remote server.
- Synchronize the entire file system of the remote server to a local directory.
- Resume interrupted synchronization processes seamlessly.
- Option to skip the MongoDB backup step.

## Prerequisites

- Python 3 installed on the local machine.
- SSH access to the remote server.
- `rsync` installed on both the local and remote machines.
- MongoDB installed on the remote server.

## Usage

### Command-Line Arguments

- `--remote_host`: The IP address or hostname of the remote server (required).
- `--remote_user`: The username for the remote server (required).
- `--remote_path`: The root directory on the remote server to be synchronized (default is `/`).
- `--local_path`: The local directory where the backup will be stored (required).
- `--backup_path`: The temporary directory on the remote server for storing MongoDB backups (default is `/tmp`).
- `--cert_path`: The path to the SSH certificate (required).
- `--nomongo`: Skip the MongoDB backup step (optional).

### Example Commands

Command Example: ```bash
python3 remote_server_backup_sync.py --remote_host 203.0.113.10 --remote_user admin --remote_path /data --local_path /home/user/remote_backup --backup_path /tmp --cert_path /home/user/.ssh/id_rsa --nomongo
```

To skip the MongoDB backup, add the `--nomongo` flag

## Notes

- Ensure that the SSH certificate specified by `--cert_path` has the necessary permissions to access the remote server.
- Verify that `rsync` is installed on both the local and remote machines.

## License

This project is open source and is available for modification and distribution under the terms of the MIT License.
