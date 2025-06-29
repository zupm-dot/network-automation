import paramiko
import re
import getpass

def ssh_run_command(host, username, password, command="show ip bgp summary"):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=username, password=password)

        stdin, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode()
        client.close()
        return output
    except Exception as e:
        print(f"[ERROR] SSH to {host} failed: {e}")
        return ""

def parse_bgp_summary(output):
    neighbors = []
    lines = output.strip().splitlines()

    for line in lines:
        if re.match(r"^\d{1,3}(\.\d{1,3}){3}", line):  # Starts with an IP
            parts = line.split()
            ip = parts[0]
            asn = parts[2]
            state_or_pfx = parts[-1]

            state = "Established" if state_or_pfx.isdigit() else state_or_pfx
            neighbors.append((ip, asn, state))

    return neighbors

# === Main Execution ===
if __name__ == "__main__":
    host = input("Router IP or Hostname: ")
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    output = ssh_run_command(host, username, password)

    if output:
        print("\nParsed BGP Neighbors:\n")
        neighbors = parse_bgp_summary(output)
        for ip, asn, state in neighbors:
            print(f"Neighbor: {ip:<15} ASN: {asn:<7} State: {state}")
    else:
        print("No output received or connection failed.")
