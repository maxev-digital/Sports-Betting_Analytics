#!/usr/bin/env python3
"""
Deploy built frontend to VPS
Copies only the critical files (index.html and assets/) that change with each build
"""
import subprocess
import sys

VPS_HOST = "root@148.230.87.135"
VPS_PATH = "/var/www/sporttrader"
LOCAL_DIST = "C:/Users/nashr/max-ev-sports/frontend/dist"

def run_ssh_command(command):
    """Execute SSH command on VPS"""
    full_cmd = f'ssh {VPS_HOST} "{command}"'
    print(f"Running: {full_cmd}")
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(result.stdout)
    return True

def deploy():
    print("=" * 80)
    print("DEPLOYING FRONTEND TO VPS")
    print("=" * 80)

    # Step 1: Backup current assets and index.html on VPS
    print("\n1. Creating backup of current frontend...")
    if not run_ssh_command(f"cd {VPS_PATH} && cp index.html index.html.backup && cp -r assets assets.backup"):
        print("Warning: Backup failed, but continuing...")

    # Step 2: Remove old assets folder on VPS
    print("\n2. Removing old assets folder...")
    if not run_ssh_command(f"rm -rf {VPS_PATH}/assets"):
        print("Error: Failed to remove old assets")
        return False

    # Step 3: Copy new index.html
    print("\n3. Copying new index.html...")
    cmd = f'scp "{LOCAL_DIST}/index.html" {VPS_HOST}:{VPS_PATH}/'
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Error: Failed to copy index.html")
        return False

    # Step 4: Copy new assets folder
    print("\n4. Copying new assets folder...")
    cmd = f'scp -r "{LOCAL_DIST}/assets" {VPS_HOST}:{VPS_PATH}/'
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print("Error: Failed to copy assets folder")
        return False

    # Step 5: Verify deployment
    print("\n5. Verifying deployment...")
    if not run_ssh_command(f"ls -lh {VPS_PATH}/assets/ | head -15"):
        print("Warning: Could not verify deployment")

    print("\n" + "=" * 80)
    print("DEPLOYMENT COMPLETE!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Test: https://max-ev-sports.com/#/predictions-database")
    print("2. Test: https://max-ev-sports.com/#/model-performance")
    print("3. Test: https://max-ev-sports.com/#/max-ev-edges")
    print("\nIf anything is broken, rollback with:")
    print(f"ssh {VPS_HOST} 'cd {VPS_PATH} && mv index.html.backup index.html && rm -rf assets && mv assets.backup assets'")

    return True

if __name__ == "__main__":
    success = deploy()
    sys.exit(0 if success else 1)
