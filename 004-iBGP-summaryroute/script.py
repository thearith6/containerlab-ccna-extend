import time
from netmiko import ConnectHandler


routers = {
    "172.20.20.11": ["interface Ethernet0/1", "ip address 10.0.12.1 255.255.255.252", "no shutdown",
                    "interface Ethernet0/2", "ip address 10.0.13.1 255.255.255.252", "no shutdown",
                    "interface lo0","ip address 1.1.1.1 255.255.255.255",
                    "router ospf 1", "network 10.0.0.0 0.0.255.255 area 0",
                    "router bgp 200","neighbor 10.0.12.2 remote-as 200",
                    "neighbor 10.0.13.2 remote-as 200",
                    "network 1.1.1.1 mask 255.255.255.255"],
    "172.20.20.12": ["interface Ethernet0/1", "ip address 10.0.12.2 255.255.255.252", "no shutdown",
                    "interface Ethernet0/2", "ip address 10.0.23.1 255.255.255.252", "no shutdown",
                    "interface lo0","ip address 2.2.2.2 255.255.255.255",
                    "router ospf 1", "network 10.0.0.0 0.0.255.255 area 0",
                    "router bgp 200","neighbor 10.0.12.1 remote-as 200",
                    "neighbor 10.0.23.2 remote-as 200"],
    "172.20.20.13": ["interface Ethernet0/1", "ip address 10.0.23.2 255.255.255.252", "no shutdown",
                    "interface Ethernet0/2", "ip address 10.0.34.1 255.255.255.252", "no shutdown",
                    "interface Ethernet0/3", "ip address 10.0.13.2 255.255.255.252", "no shutdown",
                    "interface lo0","ip address 3.3.3.3 255.255.255.255",
                    "router ospf 1", "network 10.0.0.0 0.0.255.255 area 0",
                    "ip route 10.0.0.0 255.255.0.0 Null0",
                    "router bgp 200","neighbor 10.0.34.2 remote-as 300",
                    "neighbor 10.0.23.1 remote-as 200",
                    "neighbor 10.0.13.1 remote-as 200",
                    "network 10.0.0.0 mask 255.255.0.0",
                    "neighbor 10.0.23.1 next-hop-self","neighbor 10.0.13.1 next-hop-self"],
    "172.20.20.14": ["interface Ethernet0/1", "ip address 10.0.34.2 255.255.255.252", "no shutdown",
                    "interface Ethernet0/2", "ip address 10.0.45.1 255.255.255.252", "no shutdown",
                    "interface lo0","ip address 4.4.4.4 255.255.255.255",
                    "router bgp 300","neighbor 10.0.34.1 remote-as 200", "neighbor 10.0.45.2 remote-as 400",
                    "network 4.4.4.4 mask 255.255.255.255"],
    "172.20.20.15": ["interface Ethernet0/1", "ip address 10.0.45.2 255.255.255.252", "no shutdown",
                    "interface lo0","ip address 5.5.5.5 255.255.255.255",
                    "router bgp 400","neighbor 10.0.45.1 remote-as 300", "network 5.5.5.5 mask 255.255.255.255"]
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
    time.sleep(5)
    print(ip)
    print(conn.send_command("show ip bgp"))
    conn.disconnect()
