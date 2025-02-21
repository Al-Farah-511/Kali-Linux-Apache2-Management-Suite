#!/usr/bin/env python3

import os
import subprocess
import sys
import time
from datetime import datetime

# ANSI Color Codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
RESET = "\033[0m"

LOG_FILE = "/var/log/apache2_management.log"
APACHE_LOG_DIR = "/var/log/apache2/"
CONFIG_DIR = "/etc/apache2/"
VHOST_DIR = "/etc/apache2/sites-available/"

def log_action(action, status):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {action}: {status}\n")

def print_banner():
    os.system("clear")
    print(f"""{CYAN}
    ██████╗  █████╗ ██████╗  ██████╗ ███████╗███████╗
    ██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔════╝██╔════╝
    ██████╔╝███████║██████╔╝██║   ██║█████╗  █████╗  
    ██╔═══╝ ██╔══██║██╔══██╗██║   ██║██╔══╝  ██╔══╝  
    ██║     ██║  ██║██║  ██║╚██████╔╝██║     ██║     
    ╚═╝     ╚═╝  ╚═╝╕╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝     
    {RESET}{MAGENTA}
    Kali Linux Apache2 Management Suite
    Coded By Al Farah | The 511 | Digital Security Research Group
    {RESET}""")

def print_main_menu():
    print(f"""
    {YELLOW}Main Menu:{RESET}
    [1] Service Control
    [2] Configuration Management
    [3] Log Analysis
    [4] Virtual Host Manager
    [5] Security Auditor
    [6] Advanced Tools
    [0] Exit
    """)

def service_control_menu():
    print(f"""
    {YELLOW}Service Control:{RESET}
    [1] Start Apache2
    [2] Stop Apache2
    [3] Restart Apache2
    [4] Force Reload
    [5] Detailed Status
    [6] Enable on Boot
    [7] Disable on Boot
    [8] Return to Main Menu
    """)

def execute_command(cmd, success_msg, error_msg):
    try:
        result = subprocess.run(
            cmd.split(),
            check=True,
            capture_output=True,
            text=True
        )
        print(f"{GREEN}✓ {success_msg}{RESET}")
        log_action(cmd, "Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{RED}✗ {error_msg}{RESET}")
        print(f"{YELLOW}Error: {e.stderr.strip()}{RESET}")
        log_action(cmd, f"Failed: {e.stderr.strip()}")
        return False

def advanced_tools_menu():
    print(f"""
    {YELLOW}Advanced Tools:{RESET}
    [1] Test Configuration Syntax
    [2] List Loaded Modules
    [3] Custom Systemctl Command
    [4] Network Socket Analysis
    [5] Resource Monitor
    [6] Return to Main Menu
    """)

def realtime_resource_monitor():
    try:
        print(f"{CYAN}Starting resource monitor (Ctrl+C to stop)...{RESET}")
        while True:
            os.system("clear")
            subprocess.run(["apachectl", "status"])
            time.sleep(2)
    except KeyboardInterrupt:
        pass

def analyze_logs():
    print(f"""
    {YELLOW}Log Analysis:{RESET}
    [1] View Error Log (realtime)
    [2] View Access Log (realtime)
    [3] Search Errors in Logs
    [4] Generate Traffic Report
    [5] Return to Main Menu
    """)
    
    choice = input("Select log operation: ")
    if choice == "1":
        tail_log("error.log")
    elif choice == "2":
        tail_log("access.log")

def tail_log(log_file):
    try:
        print(f"{CYAN}Tailing {log_file} (Ctrl+C to stop)...{RESET}")
        log_path = os.path.join(APACHE_LOG_DIR, log_file)
        with subprocess.Popen(["tail", "-f", log_path], 
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True) as process:
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line.strip())
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Stopped log tailing{RESET}")

def main():
    if os.geteuid() != 0:
        print(f"{RED}This script requires root privileges!{RESET}")
        sys.exit(1)

    while True:
        print_banner()
        print_main_menu()
        main_choice = input(f"{BLUE}Select operation: {RESET}")

        if main_choice == "1":
            while True:
                print_banner()
                service_control_menu()
                sc_choice = input("Service control choice: ")
                
                if sc_choice == "1":
                    execute_command("systemctl start apache2",
                                  "Apache2 started successfully",
                                  "Failed to start Apache2")
                elif sc_choice == "2":
                    execute_command("systemctl stop apache2",
                                   "Apache2 stopped successfully",
                                   "Failed to stop Apache2")
                # ... Add other service control options ...
                
                elif sc_choice == "8":
                    break

        elif main_choice == "6":
            while True:
                print_banner()
                advanced_tools_menu()
                adv_choice = input("Advanced tool choice: ")
                
                if adv_choice == "1":
                    execute_command("apachectl configtest",
                                   "Configuration test completed",
                                   "Configuration test failed")
                elif adv_choice == "5":
                    realtime_resource_monitor()
                # ... Add other advanced tools ...

        elif main_choice == "0":
            print(f"{MAGENTA}Exiting... Goodbye!{RESET}")
            sys.exit(0)

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
