#!/bin/bash

# F5 connection details
F5_HOST="<f5_host>"
F5_USER="root"
F5_PASS="<root_password>"

# Pool member IPs to clear persistence for
IPS=(
  "10.10.10.10"
  "10.10.10.20"
)

# Clear persistence records
for ip in "${IPS[@]}"; do
  echo "Deleting persistence record for node-addr $ip on $F5_HOST"
  sshpass -p "$F5_PASS" ssh -o StrictHostKeyChecking=no "$F5_USER@$F5_HOST" \
    "tmsh delete ltm persistence persist-record node-addr $ip"
done

