# 🧠 Network Automation Toolkit for Projects

- ✅ **Ansible** roles & playbooks
- 🐍 **Python** scripts for API-driven automation
- 🖥️ **Bash** scripts for fast CLI operations
- 🔁 **Postman** collections for testing & documenting REST APIs

---

## 📁 Repository Structure

```bash
network-automation/
├── ansible/
│   ├── inventories/
│   │   └── lab/
│   │       └── hosts.ini
│   ├── playbooks/
│   │   ├── configure_cisco.yml
│   │   └── deploy_f5_vip.yml
│   └── roles/
│       ├── f5_automation/
│       │   ├── templates/      # Jinja2: VIPs, pools, monitors, certs, upgrades
│       │   ├── defaults/       # Default variables
│       │   └── tasks/          # Task logic
│       └── cisco_automation/
│           ├── templates/      # Interfaces, VLANs, OSPF, ACLs, DHCP, NETCONF
│           ├── defaults/
│           └── tasks/
├── bash/
│   ├── f5/
│   │   └── f5_check_vip.sh
│   └── cisco/
│       └── get_interface_status.sh
├── python/
│   ├── f5/
│   │   └── example_create_vip.py
│   └── cisco/
│       └── example_get_interface_status.py
├── postman/
│   ├── f5/
│   │   └── f5_basic_collection.json
│   └── cisco/
│       └── cisco_basic_collection.json
└── README.md

---

## 🚀 Quickstart

### 🔧 Set up a Python environment (optional)

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests netmiko

📦 Install Ansible
pip install ansible
# Or use a requirements.yml file if defined:
# ansible-galaxy install -r requirements.yml

🧪 Run a Playbook
ansible-playbook -i ansible/inventories/lab/hosts.ini ansible/playbooks/deploy_f5_vip.yml

🔒 Sensitive Data Handling
Use group_vars/ to store variables, and Ansible Vault to encrypt secrets:

Example group_vars/all.yml:
ansible_user: admin
ansible_password: "{{ vault_admin_password }}"

Encrypt it:
ansible-vault encrypt ansible/inventories/lab/group_vars/all.yml

Decrypt or edit later:
ansible-vault edit ansible/inventories/lab/group_vars/all.yml

🧰 Use Cases
Task	                Tool/Role	        File(s)
Create F5 VIP	        Ansible + Python	vip.j2, example_create_vip.py
Cisco VLAN Config	Ansible	                vlan_config.j2
Code Upgrade on F5	Ansible	                code_upgrade.j2
Check VIP via CLI	Bash	                f5_check_vip.sh
Cisco Interface Status	Python	                example_get_interface_status.py
REST API Testing	Postman	                f5_basic_collection.json

🧠 References
🌐 Cisco DevNet
📘 F5 Automation Docs
⚙️ Ansible for Network Automation
🧪 Postman API Platform
