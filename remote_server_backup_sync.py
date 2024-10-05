import os
import subprocess
import datetime
import shlex
import argparse

def run_command(command):
    try:
        subprocess.run(shlex.split(command), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing: {command}\nError: {e}")

def backup_mongodb(remote_host, remote_user, backup_path, cert_path):
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
    dump_path = f"{backup_path}/mongodb_backup_{timestamp}"
    command = f"ssh -i {shlex.quote(cert_path)} {shlex.quote(remote_user)}@{shlex.quote(remote_host)} mongodump --out {shlex.quote(dump_path)}"
    run_command(command)
    return dump_path

def sync_server(remote_host, remote_user, remote_path, local_path, cert_path):
    exclude_paths = ["/proc", "/sys", "/dev"]
    exclude_flags = ' '.join([f"--exclude={path}" for path in exclude_paths])
    command = (
        f"rsync -avz {exclude_flags} --progress --partial --delete -e 'ssh -i {shlex.quote(cert_path)}' "
        f"{shlex.quote(remote_user)}@{shlex.quote(remote_host)}:{shlex.quote(remote_path)} {shlex.quote(local_path)}"
    )
    run_command(command)

def main():
    parser = argparse.ArgumentParser(description="Backup and sync remote server data.")
    parser.add_argument("--remote_host", required=True, help="The IP or hostname of the remote server.")
    parser.add_argument("--remote_user", required=True, help="The username for the remote server.")
    parser.add_argument("--remote_path", default="/", help="The root path of the remote server to sync.")
    parser.add_argument("--local_path", required=True, help="The local path to store the backup.")
    parser.add_argument("--backup_path", default="/tmp", help="The temporary backup path for MongoDB on the remote server.")
    parser.add_argument("--cert_path", required=True, help="The path to the SSH certificate.")
    parser.add_argument("--nomongo", action="store_true", help="Skip the MongoDB backup step.")

    args = parser.parse_args()

    # Step 1: Backup MongoDB on the remote server if --nomongo is not specified
    if not args.nomongo:
        print("Starting MongoDB backup...")
        mongodb_backup_path = backup_mongodb(args.remote_host, args.remote_user, args.backup_path, args.cert_path)
        print(f"MongoDB backup completed: {mongodb_backup_path}")

    # Step 2: Sync the entire server to the local PC, including the MongoDB backup if performed
    print("Starting server synchronization...")
    sync_server(args.remote_host, args.remote_user, args.remote_path, args.local_path, args.cert_path)
    print("Server synchronization completed.")

if __name__ == "__main__":
    main()
