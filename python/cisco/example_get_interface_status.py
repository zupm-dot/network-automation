#!/usr/bin/env python3
from netmiko import ConnectHandler

def get_interface_status(host, user, password, interface):
    device = {
        "device_type": "cisco_ios",
        "host": host,
        "username": user,
        "password": password,
    }
    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command(f"show interface {interface} status")
        print(output)

if __name__ == "__main__":
    get_interface_status("192.168.1.10", "admin", "admin", "GigabitEthernet1")

