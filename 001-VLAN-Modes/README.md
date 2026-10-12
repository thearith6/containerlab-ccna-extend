# 001-VLAN-Modes

Simple VLAN configurations automation using python.

## Scenario
``` mermaid
graph TD
SW1---SW2
SW1---pc1
SW1---pc2
SW2---pc3
SW2---pc4
```

```Each SW connect to 2 end hosts, and interconnected by a trunk.
  SW1:
    e0/2 --- pc1 (VLAN 10) 192.168.10.10/24
    e0/3 --- pc2 (VLAN 20) 192.168.20.10/24
  SW2:
    e0/2 --- pc3 (VLAN 10) 192.168.10.20/24
    e0/3 --- pc4 (VLAN 20) 192.168.20.20/24
  SW1: e0/1 --- SW2: e0/2 (Trunk)
```

## Action
1. Topology Building  [YAML File](001-VLAN-MODES.clab.yml):
```
  topology:
    nodes:
      SW1, SW2, SW3, SW4, pc1, pc2, pc3, pc4
    links:
      endpoints: [sw1,sw2], [sw1,pc1], [sw1,pc2]
                 [sw2,pc3], [sw2,pc4]
```

2. Configuration [Python Script](script.py):
```
Two main functions, one for Switch, one for end hosts.
  1. Switch: Loop through SW1 and SW2, identical configurations (vlan, switchport modes, trunk).
  2. Hosts:
    - Define each host with an ip/mask.
    - Loop through each host, push ip/mask and enable interface.
```

## Result
1. Linux alpine:
  - Open shell: `docker exec -it clab.name.pc sh`
  - Use subprocess, can't push config via ssh like SW.
  - Manual ip setup: `ip addr add ip/mask dev eth1`, `ip link set eth1 up`

2. Containerlab: Switch interface use e or Ethernet. 
3. LAB:
  - Ping Result:
  ```/ # ping 192.168.10.20
  PING 192.168.10.20 (192.168.10.20): 56 data bytes
  64 bytes from 192.168.10.20: seq=0 ttl=64 time=0.480 ms
  64 bytes from 192.168.10.20: seq=1 ttl=64 time=1.075 ms
  64 bytes from 192.168.10.20: seq=2 ttl=64 time=1.134 ms
  ```
  
  - Trunk:
  ```
  Port           Mode             Encapsulation  Status        Native vlan
  Et0/1          on               802.1q         trunking      1
  
  Port           Vlans allowed on trunk
  Et0/1          10,20
  
  Port           Vlans allowed and active in management domain
  Et0/1          10,20
  
  Port           Vlans in spanning tree forwarding state and not pruned
  Et0/1          10,20
  ```
  
  - VLAN Brief:
  ```
  VLAN Name                             Status    Ports
  ---- -------------------------------- --------- -------------------------------
  1    default                          active
  10   HR                               active    Et0/2
  20   IT                               active    Et0/3
  1002 fddi-default                     act/unsup
  1003 token-ring-default               act/unsup
  1004 fddinet-default                  act/unsup
  1005 trnet-default                    act/unsup
  ```
