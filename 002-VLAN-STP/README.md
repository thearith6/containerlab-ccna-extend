# 002-VLAN-STP
Basic spanning-tree configurations.

## Scenario
``` mermaid
graph LR
SW1---|"e0/2 ↔ e0/1"|SW2
SW1---|"e0/3 ↔ e0/1"|SW3
SW2---|"e0/3 ↔ e0/2"|SW3
```

```
SW1, SW2, SW3 connected by trunk links, allowed VLAN 10 and VLAN 20.
SW1 as root bridge for VLAN 10.
SW3 as root bridge for VLAN 20.
SW2 as secondary root for both VLANs.
```
## Action
1. Topology Building  [YAML File](002-VLAN-STP.clab.yml):
```
  topology:
    nodes:
      SW1, SW2, SW3
    links:
      endpoints: [sw1,sw2], [sw1,sw3], [sw2,sw3]
                
```

2. Configuration [Python Script](script.py):
```
Loop through SW1 and SW2, and SW3. 
    1. Identical configurations (vlans, trunk links).
    2. Lowest priority win stp root election:
      - VLAN 10: stp priority increase as index increment (i * 4096)
      - VLAN 20: stp priority decrease as index increment ((2-i) * 4096)

```
## Result
1. VLAN 10: stp priority increase as index increment (i * 4096):
  - SW1 priority=0+10 (root bridge),
  - SW2 priority=4096+10 (root secondary)
  - SW3 priority=8192+10 (root tertiary)
2. VLAN 20: stp priority decrease as index increment ((2-i) * 4096):
  - SW3 priority=0+20 (root bridge),
  - SW2 priority=4096+20 (root secondary)
  - SW1 priority=8192+20 (root tertiary)

3. LAB:
  - VLAN 10 stp:
  ```
  SW1#show spanning-tree vlan 10
  VLAN0010
    Spanning tree enabled protocol rstp
    Root ID    Priority    10
               Address     aabb.cc00.0100
               This bridge is the root
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
  
    Bridge ID  Priority    10     (priority 0 sys-id-ext 10)
               Address     aabb.cc00.0100
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
               Aging Time  300 sec
  
  Interface           Role Sts Cost      Prio.Nbr Type
  ------------------- ---- --- --------- -------- --------------------------------
  Et0/1               Desg FWD 100       128.2    P2p
  Et0/2               Desg FWD 100       128.3    P2p
  Et0/3               Desg FWD 100       128.4    P2p
  ```
  ```
  SW2#show spanning-tree vlan 10
  VLAN0010
    Spanning tree enabled protocol rstp
    Root ID    Priority    10
               Address     aabb.cc00.0100
               Cost        100
               Port        2 (Ethernet0/1)
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
  
    Bridge ID  Priority    4106   (priority 4096 sys-id-ext 10)
               Address     aabb.cc00.0200
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
               Aging Time  300 sec
  
  Interface           Role Sts Cost      Prio.Nbr Type
  ------------------- ---- --- --------- -------- --------------------------------
  Et0/1               Root FWD 100       128.2    P2p
  Et0/2               Desg FWD 100       128.3    P2p
  Et0/3               Desg FWD 100       128.4    P2p
  ```
  ```
  SW3#show spanning-tree vlan 10
  VLAN0010
    Spanning tree enabled protocol rstp
    Root ID    Priority    10
               Address     aabb.cc00.0100
               Cost        100
               Port        2 (Ethernet0/1)
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
  
    Bridge ID  Priority    8202   (priority 8192 sys-id-ext 10)
               Address     aabb.cc00.0300
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
               Aging Time  300 sec
  
  Interface           Role Sts Cost      Prio.Nbr Type
  ------------------- ---- --- --------- -------- --------------------------------
  Et0/1               Root FWD 100       128.2    P2p
  Et0/2               Altn BLK 100       128.3    P2p
  Et0/3               Desg FWD 100       128.4    P2p
  ```
  - VLAN 20 stp:
  ```
  SW1#show spanning-tree vlan 20
  
  VLAN0020
    Spanning tree enabled protocol rstp
    Root ID    Priority    20
               Address     aabb.cc00.0300
               Cost        100
               Port        4 (Ethernet0/3)
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
  
    Bridge ID  Priority    8212   (priority 8192 sys-id-ext 20)
               Address     aabb.cc00.0100
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
               Aging Time  300 sec
  
  Interface           Role Sts Cost      Prio.Nbr Type
  ------------------- ---- --- --------- -------- --------------------------------
  Et0/1               Desg FWD 100       128.2    P2p
  Et0/2               Altn BLK 100       128.3    P2p
  Et0/3               Root FWD 100       128.4    P2p
  ```
  ```
  SW2#show spanning-tree vlan 20
  VLAN0020
    Spanning tree enabled protocol rstp
    Root ID    Priority    20
               Address     aabb.cc00.0300
               Cost        100
               Port        4 (Ethernet0/3)
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
  
    Bridge ID  Priority    4116   (priority 4096 sys-id-ext 20)
               Address     aabb.cc00.0200
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
               Aging Time  300 sec
  
  Interface           Role Sts Cost      Prio.Nbr Type
  ------------------- ---- --- --------- -------- --------------------------------
  Et0/1               Desg FWD 100       128.2    P2p
  Et0/2               Desg FWD 100       128.3    P2p
  Et0/3               Root FWD 100       128.4    P2p
  ```
  ```
  SW3#show spanning-tree vlan 20
  VLAN0020
    Spanning tree enabled protocol rstp
    Root ID    Priority    20
               Address     aabb.cc00.0300
               This bridge is the root
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
  
    Bridge ID  Priority    20     (priority 0 sys-id-ext 20)
               Address     aabb.cc00.0300
               Hello Time   2 sec  Max Age 20 sec  Forward Delay 15 sec
               Aging Time  300 sec
  
  Interface           Role Sts Cost      Prio.Nbr Type
  ------------------- ---- --- --------- -------- --------------------------------
  Et0/1               Desg FWD 100       128.2    P2p
  Et0/2               Desg FWD 100       128.3    P2p
  Et0/3               Desg FWD 100       128.4    P2p
  ```
