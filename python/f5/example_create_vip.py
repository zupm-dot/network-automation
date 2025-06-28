#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def create_vip(host, user, password, vip_name, vip_ip, vip_port):
    url = f"https://{host}/mgmt/tm/ltm/virtual"
    payload = {
        "name": vip_name,
        "destination": f"/Common/{vip_ip}:{vip_port}",
        "ipProtocol": "tcp",
        "pool": "pool_app1"
    }
    resp = requests.post(url, auth=HTTPBasicAuth(user, password), json=payload, verify=False)
    if resp.status_code in [200, 201]:
        print(f"VIP {vip_name} created successfully")
    else:
        print(f"Failed to create VIP: {resp.text}")

if __name__ == "__main__":
    create_vip("f5-lb1", "admin", "admin", "vip_app1", "10.10.10.100", 443)

