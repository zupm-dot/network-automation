#!/bin/bash
# Usage: ./f5_check_vip.sh <F5_HOST> <USERNAME> <PASSWORD> <VIP_NAME>
F5_HOST=$1
USER=$2
PASS=$3
VIP_NAME=$4

if [[ -z "$F5_HOST" || -z "$USER" || -z "$PASS" || -z "$VIP_NAME" ]]; then
  echo "Usage: $0 <F5_HOST> <USERNAME> <PASSWORD> <VIP_NAME>"
  exit 1
fi

curl -sk -u "$USER:$PASS" "https://$F5_HOST/mgmt/tm/ltm/virtual/~Common~$VIP_NAME" | jq .

