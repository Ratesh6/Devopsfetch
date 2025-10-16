#!/usr/bin/env python3
import os
import subprocess
from datetime import datetime

LOG_DIR = "/opt/devopsfetch/logs"
MAIN_LOG = "/var/log/devopsfetch/devopsfetch.log"
ERR_LOG = "/var/log/devopsfetch/devopsfetch.err"

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_snapshot():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MAIN_LOG, "a") as f:
        f.write(f"\n===== System Snapshot: {timestamp} =====\n")
        # Ports listening
        ports = subprocess.getoutput("ss -tuln")
        f.write("Ports:\n" + ports + "\n")
        # Docker containers
        docker = subprocess.getoutput("docker ps --no-trunc")
        f.write("Docker:\n" + docker + "\n")
        # Nginx processes
        nginx = subprocess.getoutput("ps aux | grep nginx")
        f.write("Nginx Processes:\n" + nginx + "\n")
    # Update individual logs
    update_individual_logs()

def update_individual_logs():
    # Ports log
    ports = subprocess.getoutput("ss -tuln | grep LISTEN")
    with open(f"{LOG_DIR}/ports.log", "w") as f:
        f.write(ports)
    
    # Docker log
    docker = subprocess.getoutput("docker ps --no-trunc")
    with open(f"{LOG_DIR}/docker.log", "w") as f:
        f.write(docker)
    
    # Nginx logs
    if os.path.exists("/var/log/nginx/access.log"):
        try:
            subprocess.run(["cp", "/var/log/nginx/access.log", f"{LOG_DIR}/nginx_access.log"], check=True)
        except:
            open(f"{LOG_DIR}/nginx_access.log", "w").close()
    else:
        open(f"{LOG_DIR}/nginx_access.log", "w").close()
    
    if os.path.exists("/var/log/nginx/error.log"):
        try:
            subprocess.run(["cp", "/var/log/nginx/error.log", f"{LOG_DIR}/nginx_error.log"], check=True)
        except:
            open(f"{LOG_DIR}/nginx_error.log", "w").close()
    else:
        open(f"{LOG_DIR}/nginx_error.log", "w").close()
    
    # Script error log
    if os.path.exists(ERR_LOG):
        subprocess.run(["cp", ERR_LOG, f"{LOG_DIR}/devopsfetch.err"])
    else:
        open(f"{LOG_DIR}/devopsfetch.err", "w").close()
    
    # Make logs readable
    subprocess.run(["chmod", "-R", "o+r", LOG_DIR])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--monitor", action="store_true", help="Take snapshot and update logs")
    args = parser.parse_args()
    if args.monitor:
        log_snapshot()
        print("Logged system snapshot.")
