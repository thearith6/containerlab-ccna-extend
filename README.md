# Containerlab Networking Labs with Python Automation

Small network labs built with [Containerlab](https://containerlab.dev/). Each lab deploys a topology from a YAML file and configures it with a Python script using [Netmiko](https://github.com/ktbyers/netmiko). The labs cover CCNA-level switching (VLANs, spanning tree) and basic BGP, with OSPF as the underlying IGP in one of them.

## Labs

| Lab | Topic | What it covers | Status |
| :--- | :--- | :--- | :--- |
| [simple_script](simple_script/) | Netmiko basics | Two routers and two hosts; a script configures interfaces and eBGP between two ASes, then prints `show ip bgp summary` | Done |
| [001-VLAN-Modes](001-VLAN-Modes/) | VLANs | Access ports, an 802.1Q trunk, and Alpine hosts configured through `docker exec` | Done |
| [002-VLAN-STP](002-VLAN-STP/) | Spanning Tree | Per-VLAN root bridge and secondary root priorities on three switches (Rapid PVST+) | Done |
| [003-iBGP-nexthopself](003-iBGP-nexthopself/) | BGP | eBGP across three ASes; why an iBGP edge router needs `next-hop-self` | Done |
| [004-BGP-summaryroute](004-BGP-summaryroute/) | BGP | OSPF as the iGP inside AS 200 and an aggregate `network` statement that needs a `Null0` static route | Done |

## Requirements

- Linux with [Docker](https://docs.docker.com/engine/install/) and [Containerlab](https://containerlab.dev/install/)
- Router and switch images built with [vrnetlab](https://github.com/srl-labs/vrnetlab). The images are **not included** in this repository. The labs expect:
  - `vrnetlab/cisco_iol:17.18.2` (L3) and `vrnetlab/cisco_iol:L2-17.18.2` (L2), built from your own Cisco IOL files
- Python 3.12 with Netmiko (`pip install -r requirements.txt`)

## Running a lab

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cd 003-iBGP-nexthopself
sudo containerlab deploy -t 003-iBGP-nexthopself.clab.yml
python3 script.py          # waits for the nodes to boot, then pushes the configuration
sudo containerlab destroy -t 003-iBGP-nexthopself.clab.yml --cleanup
```

Notes:
- Labs 001–004 pin the management addresses in the YAML (`172.20.20.0/24`), and the scripts use those addresses. `simple_script` does not pin them, so check the addresses with `containerlab inspect` and edit the IPs in `script.py` if they differ.
- The scripts log in with `admin` / `admin`, the default credentials of the vrnetlab images. They are lab defaults, not real credentials.

## Lab format

Every lab README follows the same three sections:

- **Scenario:** topology and the goal
- **Action:** the configuration steps and the script that applies them
- **Result:** verification output (`show` commands, ping) and what I learned

## Layout

```
NNN-lab-name/
├── NNN-lab-name.clab.yml   # Containerlab topology
├── script.py               # Netmiko configuration script
└── README.md               # Scenario, Action, Result
sample_script.py            # Extra example: four-router eBGP configuration script
```
