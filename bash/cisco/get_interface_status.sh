#!/bin/bash
# Usage: ./get_interface_status.sh <DEVICE_IP> <USERNAME> <PASSWORD> <INTERFACE>
DEVICE_IP=$1
USER=$2
PASS=$3
INTERFACE=$4

if [[ -z "$DEVICE_IP" || -z "$USER" || -z "$PASS" || -z "$INTERFACE" ]]; then
  echo "Usage: $0 <DEVICE_IP> <USERNAME> <PASSWORD> <INTERFACE>"
  exit 1
fi

sshpass -p "$PASS" ssh -o StrictHostKeyChecking=no "$USER@$DEVICE_IP" "show interface $INTERFACE status"

