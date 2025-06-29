# usage: python3 get_certificate_expirations.py <hostname> <root account>

import paramiko
import sys
import re
import json
from datetime import datetime, timezone, timedelta

def ssh_run_command(client, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    return stdout.read().decode('utf-8'), stderr.read().decode('utf-8')

def parse_certs(raw_output):
    certs = []
    partition = None
    cert = {}
    for line in raw_output.splitlines():
        # Partition header line
        part_match = re.match(r'^>>>PARTITION: (\S+)', line)
        if part_match:
            partition = part_match.group(1)
            continue

        # Start of cert block
        cert_start = re.match(r'^sys file ssl-cert (\S+)', line)
        if cert_start:
            if cert and 'expiration' in cert:
                certs.append(cert)
            cert = {
                'name': cert_start.group(1),
                'partition': partition,
                'issuer': '',
                'subject': '',
                'expiration': '',
            }
            continue

        # expiration-string line
        exp_match = re.match(r'^\s*expiration-string\s+"(.+)"', line)
        if exp_match:
            cert['expiration'] = exp_match.group(1)
            continue

        # issuer line
        issuer_match = re.match(r'^\s*issuer\s+"(.+)"', line)
        if issuer_match:
            cert['issuer'] = issuer_match.group(1)
            continue

        # subject line
        subject_match = re.match(r'^\s*subject\s+"(.+)"', line)
        if subject_match:
            cert['subject'] = subject_match.group(1)
            continue

        # ignore subject-alternative-name
    # Add last cert if exists
    if cert and 'expiration' in cert:
        certs.append(cert)
    return certs

def extract_cn(subject):
    m = re.search(r'CN=([^,]+)', subject)
    return m.group(1) if m else "-"

def main(f5_host, username):
    # Connect SSH
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(f5_host, username=username)
    except Exception as e:
        print(f"SSH connection failed: {e}")
        sys.exit(1)

    # Get list of partitions
    partitions_out, _ = ssh_run_command(client, 'tmsh list auth partition | grep "^auth partition" | awk \'{print $3}\'')
    partitions = partitions_out.strip().splitlines()

    raw_output = ""
    for p in partitions:
        raw_output += f">>>PARTITION: {p}\n"
        # List all certs in partition p
        cmd = f'tmsh -q -c "cd /{p}; list sys file ssl-cert all"'
        part_out, err = ssh_run_command(client, cmd)
        raw_output += part_out

    client.close()

    # Parse certs
    certs = parse_certs(raw_output)

    now = datetime.now(timezone.utc)
    threshold = now + timedelta(days=30)

    expiring_certs = []
    for cert in certs:
        try:
            exp_date = datetime.strptime(cert['expiration'], '%b %d %H:%M:%S %Y GMT').replace(tzinfo=timezone.utc)
        except ValueError:
            # Some dates might have single digit day with two spaces, try fixing that
            try:
                fixed_date = re.sub(r'(\w{3})  (\d{1})', r'\1 \2', cert['expiration'])
                exp_date = datetime.strptime(fixed_date, '%b %d %H:%M:%S %Y GMT').replace(tzinfo=timezone.utc)
            except Exception:
                # If still fails, skip this cert
                continue

        if now <= exp_date <= threshold:
            expiring_certs.append({
                "partition": cert['partition'],
                "common_name": extract_cn(cert['subject']),
                "subject": cert['subject'],
                "issuer": cert['issuer'],
                "expiration": cert['expiration']
            })

    output = {
        "hostname": f5_host,
        "expiring_certificates": expiring_certs
    }

    with open("expiring_certs.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Done. Expiring certificates saved in: expiring_certs.json")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <f5-hostname> <username>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
