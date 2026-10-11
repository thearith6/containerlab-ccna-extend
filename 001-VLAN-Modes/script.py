import time
import subprocess
from netmiko import ConnectHandler

LAB = "clab-001-VLAN-Modes"

SWITCH_CONFIG = [
    "vlan 10", "name HR", "vlan 20", "name IT",
    "interface Ethernet0/2", "switchport mode access", "switchport access vlan 10",
    "interface Ethernet0/3", "switchport mode access", "switchport access vlan 20",
    "interface Ethernet0/1", "sw trunk encap dot1q", "sw trunk allow vlan 10,20", "sw mode trunk",
    "do wr",
]

switches = ["172.20.20.11", "172.20.20.12"]

hosts = {
    "pc1": "192.168.10.10/24",
    "pc2": "192.168.20.10/24",
    "pc3": "192.168.10.20/24",
    "pc4": "192.168.20.20/24",
}


def config_host(name, ip):
    for cmd in [f"ip addr add {ip} dev eth1", "ip link set eth1 up"]:
        subprocess.run(["docker", "exec", f"{LAB}-{name}", "sh", "-c", cmd])


def connect(ip):
    for attempt in range(20):
        try:
            return ConnectHandler(device_type="cisco_ios", host=ip,
                                  username="admin", password="admin")
        except Exception:
            print(ip, "not ready, waiting 15s...")
            time.sleep(15)
    raise RuntimeError(f"Could not connect to {ip}")


def config_switch(ip, cmds):
    conn = connect(ip)
    conn.send_config_set(cmds)
    time.sleep(5)
    print(ip)
    print(conn.send_command("show ip interface brief"))
    conn.disconnect()


for name, ip in hosts.items():
    config_host(name, ip)

for ip in switches:
    config_switch(ip, SWITCH_CONFIG)
