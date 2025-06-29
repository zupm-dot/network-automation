#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
BOLD='\033[1m'
RESET='\033[0m'

HORIZON_FQDN="example.yourorg.com"

echo -e "${BOLD}${CYAN}▶ Checking Pool Members and VIP${RESET}"

# Loop through Pool Members
for ip in 10.10.10.10 10.10.10.20; do
  fqdn=$(dig +short -x "$ip" | sed 's/\.$//')
  [[ -z "$fqdn" ]] && fqdn="unresolved"

  output=$(curl -sk --connect-timeout 5 -X POST \
    --resolve ${HORIZON_FQDN}:443:$ip \
    -H "Host: " \
    -H "Content-Type: text/xml" \
    -H "User-Agent: VMware View Client" \
    -d '<BrokerProtocol version="2.0"><Request><GetCapabilities/></Request></BrokerProtocol>' \
    -w "CURL_HTTP_CODE:%{http_code}" \
    -D - https://${HORIZON_FQDN}/broker/xml -o /tmp/pool_response_body.txt)

  http_status=$(echo "$output" | grep -i "^HTTP" | tail -n1 | awk '{print $2}')
  x_served_by=$(echo "$output" | grep -i "^X-Served-By" | cut -d' ' -f2-)
  curl_http_code=$(echo "$output" | grep "CURL_HTTP_CODE" | cut -d':' -f2)

  echo -e "${YELLOW}→ Pool Member: ${BOLD}$ip${RESET}"
  echo -e "   ${BLUE}FQDN:       ${RESET}$fqdn"

  if [[ -z "$http_status" || "$curl_http_code" == "000" ]]; then
    echo -e "   ${RED}HTTP Status: ${RESET}No response (Pool Member is DOWN)"
    echo -e "   ${RED}HTTP Code:   ${RESET}000"
  else
    if [[ "$http_status" == "200" ]]; then
      echo -e "   ${GREEN}HTTP Status: ${RESET}$http_status"
    else
      echo -e "   ${RED}HTTP Status: ${RESET}$http_status"
    fi

    if [[ "$curl_http_code" == "200" ]]; then
      echo -e "   ${GREEN}HTTP Code:   ${RESET}$curl_http_code"
    else
      echo -e "   ${RED}HTTP Code:   ${RESET}$curl_http_code"
    fi
  fi

  if [[ "$x_served_by" != "self" && -n "$x_served_by" ]]; then
    echo -e "   ${CYAN}X-Served-By: ${RESET}$x_served_by"
  fi

  echo
done

# VIP Section
vip_ip="192.168.1.100"
vip_fqdn=$(dig +short -x "$vip_ip" | sed 's/\.$//')
[[ -z "$vip_fqdn" ]] && vip_fqdn="unresolved"

vip_output=$(curl -sk --connect-timeout 5 \
  --resolve ${HORIZON_FQDN}:443:$vip_ip \
  -H "Host: ${HORIZON_FQDN}" \
  -w "CURL_HTTP_CODE:%{http_code}" \
  -D - https://${HORIZON_FQDN} -o /tmp/vip_response_body.txt)

vip_http_status=$(echo "$vip_output" | grep -i "^HTTP" | tail -n1 | awk '{print $2}')
vip_served_by=$(echo "$vip_output" | grep -i "^X-Served-By" | cut -d' ' -f2-)
vip_code=$(echo "$vip_output" | grep "CURL_HTTP_CODE" | cut -d':' -f2)

echo -e "${MAGENTA}→ LB VIP IP:  ${BOLD}$vip_ip${RESET}"
echo -e "   ${BLUE}FQDN:        ${RESET}$vip_fqdn"

if [[ -z "$vip_http_status" || "$vip_code" == "000" ]]; then
  echo -e "   ${RED}HTTP Status: ${RESET}No response (VIP is DOWN)"
  echo -e "   ${RED}HTTP Code:   ${RESET}000"
else
  if [[ "$vip_http_status" == "200" ]]; then
    echo -e "   ${GREEN}HTTP Status: ${RESET}$vip_http_status"
  else
    echo -e "   ${RED}HTTP Status: ${RESET}$vip_http_status"
  fi

  if [[ "$vip_code" == "200" ]]; then
    echo -e "   ${GREEN}HTTP Code:   ${RESET}$vip_code"
  else
    echo -e "   ${RED}HTTP Code:   ${RESET}$vip_code"
  fi
fi

if [[ "$vip_served_by" != "self" && -n "$vip_served_by" ]]; then
  echo -e "   ${YELLOW}X-Served-By: ${RESET}$vip_served_by"
fi

echo
