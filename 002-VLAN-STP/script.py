import time
from netmiko import ConnectHandler


switches = [
    "172.20.20.11",
    "172.20.20.12",
    "172.20.20.13"
]

for i, ip in enumerate(switches):
    conn = None
    for attempt in range(20):
        try:
            conn = ConnectHandler(device_type="cisco_ios", host=ip,
                                  username="admin", password="admin")
            break
        except Exception:
            print(ip, "not ready, waiting 15s...")
            time.sleep(15)

    if conn is None:
        print(ip, "never came up, skipping")
        continue

    conn.send_config_set(
            [
            "vlan 10", "name HR",
            "vlan 20", "name IT",
            "interface ra e0/1-3",
            "sw trunk encap dot1q",
            "sw trunk allowed vlan 10,20",
            "sw mode trunk"
        ]
    )

    conn.send_config_set(
            [
            f"spanning-tree vlan 10 priority {i * 4096}",
            f"spanning-tree vlan 20 priority {(2-i) * 4096}",
            "spanning-tree mode rapid-pvst",
            "spanning-tree portfast default",
            "spanning-tree portfast bpdu-guard default"
        ]
    )
    time.sleep(5)
    print(ip)
    print(conn.send_command("show vlan br"))
    print(conn.send_command("show spanning-tree vlan 10 sum"))
    conn.disconnect()
