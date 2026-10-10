import time
from netmiko import ConnectHandler

routers = {
    "172.20.20.5": [
        "interface Ethernet0/1", "ip address 192.168.1.1 255.255.255.0", "no shutdown",
        "interface Ethernet0/2", "ip address 10.0.13.1 255.255.255.252", "no shutdown",
        "router bgp 65001", "neighbor 10.0.13.2 remote-as 65003",
        "network 192.168.1.0 mask 255.255.255.0",
    ],
    "172.20.20.6": [
        "interface Ethernet0/1", "ip address 10.0.34.1 255.255.255.252", "no shutdown",
        "interface Ethernet0/2", "ip address 10.0.13.2 255.255.255.252", "no shutdown",
        "router bgp 65003", "neighbor 10.0.13.1 remote-as 65001", "neighbor 10.0.34.2 remote-as 65004",  
    ],
    "172.20.20.7": [
        "interface Ethernet0/1", "ip address 10.0.24.1 255.255.255.252", "no shutdown",
        "interface Ethernet0/2", "ip address 10.0.34.2 255.255.255.252", "no shutdown",
        "router bgp 65004", "neighbor 10.0.34.1 remote-as 65003", "neighbor 10.0.24.2 remote-as 65002",  
    ],
    "172.20.20.4": [
        "interface Ethernet0/1", "ip address 192.168.2.1 255.255.255.0", "no shutdown",
        "interface Ethernet0/2", "ip address 10.0.24.2 255.255.255.252", "no shutdown",
        "router bgp 65002", "neighbor 10.0.24.1 remote-as 65004",
        "network 192.168.2.0 mask 255.255.255.0",
    ],
}

for ip, cmds in routers.items():
    for attempt in range(20):
        try:
            conn = ConnectHandler(device_type="cisco_ios", host=ip,
                                  username="admin", password="admin")
            break
        except Exception:
            print(ip, "not ready, waiting 15s...")
            time.sleep(15)
    conn.send_config_set(cmds)
    time.sleep(10)
    print(ip)
    print(conn.send_command("show ip bgp summary"))
    conn.disconnect()