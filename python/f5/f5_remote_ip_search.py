# usage: 
# create a file called _f5_hosts.txt and populate
# create a file called _ip_list.txt and populate

import paramiko
import getpass
import re

# Load F5 hostnames from file
with open("_f5_hosts.txt", "r") as file:
    f5_hosts = [line.strip() for line in file if line.strip()]

# Load IPs and build grep pattern
with open("_ip_list.txt", "r") as file:
    ip_list = [line.strip() for line in file if line.strip()]
grep_pattern = r'\\|'.join(ip_list)

# Prompt for F5 username and passwords
f5_user = input("Enter F5 username: ")
default_password = getpass.getpass(f"Enter default password for {f5_user}: ")
special_password = getpass.getpass("Enter password for special_host: ")

# Remote command to execute
remote_command = f"""tmsh -q -c 'cd /; show running-config recursive' | grep "{grep_pattern}" """

# SSH function with keyboard-interactive auth
def ssh_run_command(host, user, password, command):
    print(f"\n------ Connecting to {host} ------")
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect()

        def handler(title, instructions, prompt_list):
            return [password if "Password" in prompt or not show_input else input(prompt)
                    for prompt, show_input in prompt_list]

        transport.auth_interactive(user, handler)

        session = transport.open_session()
        session.exec_command(command)
        stdout = session.makefile().read().decode()
        stderr = session.makefile_stderr().read().decode()

        if stdout:
            # Only show unique IP matches
            matches = [ip for ip in ip_list if ip in stdout]
            unique_matches = sorted(set(matches))
            if unique_matches:
                print("Matches found:")
                for match in unique_matches:
                    print(f"- {match}")
            else:
                print("No matches found.")
        if stderr:
            print("Errors:", stderr.strip())

        session.close()
        transport.close()

    except Exception as e:
        print(f"Failed to connect to {host}: {str(e)}")

# Loop through all F5 hosts
for host in f5_hosts:
    password = special_password if host == "cdc-1-cce-lb-1.midwestiso.org" else default_password
    ssh_run_command(host, f5_user, password, remote_command)
