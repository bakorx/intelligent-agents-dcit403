# Lab 2 — Environment and Agent Platform Setup

**Objective**
- Set up the development environment and verify a minimal SPADE-based fire sensor agent runs and logs fire incident percepts.

**Environment**
- Platform: GitHub Codespaces (Ubuntu container). Use the workspace Python (`python --version`) provided by Codespaces.
- Dependencies: Install with:
```bash
/bin/python3 -m pip install spade --break-system-packages
```
- SPADE: Listed in `requirements.txt` and used for agent scaffolding.
- XMPP credentials used in examples:
  - JID: agentbakor@xmpp.jp
  - Password: bakoragent

**Provided files & purpose**
- `sensor_agent.py`: A SPADE `SensorAgent` that periodically generates simulated fire incident percepts (dicts with `timestamp`, `severity`, `damage`, `fire_type`, `location`, `spread_rate`, and `casualties`) and appends them to `event_logs.txt`.
- `run_agent.sh`: Helper to run the agent in background and redirect logs (see repository root).
- `event_logs.txt`: Accumulated fire sensor percepts (created by the sensor agent).

**Fire Percept Fields**
| Field | Description | Example Values |
|---|---|---|
| `timestamp` | UTC time of detection | `2026-02-19T14:28:04Z` |
| `severity` | Fire severity level | `none`, `low`, `medium`, `high`, `critical` |
| `damage` | Estimated damage (0–100) | `79` |
| `fire_type` | Type of fire detected | `structural`, `wildfire`, `electrical`, `chemical`, `vehicle` |
| `location` | Location of the fire | `Block A`, `Block B`, `Warehouse`, `Forest Zone`, `Industrial Park` |
| `spread_rate` | Fire spread in metres/min | `6.3` |
| `casualties` | Number of casualties (non-zero for high/critical only) | `4` |

**How to run**
1. Install requirements:
```bash
/bin/python3 -m pip install spade --break-system-packages
```
2. Start the fire sensor agent (period default 5s):
```bash
python3 sensor_agent.py --period 2
```
3. Tail the logs:
```bash
tail -f event_logs.txt
```

**Sample log entries**
```
{'timestamp': '2026-01-29T09:43:32Z', 'severity': 'low', 'damage': 17, 'fire_type': 'electrical', 'location': 'Block A', 'spread_rate': 1.2, 'casualties': 0}
{'timestamp': '2026-01-29T09:49:02Z', 'severity': 'critical', 'damage': 99, 'fire_type': 'wildfire', 'location': 'Forest Zone', 'spread_rate': 9.8, 'casualties': 12}
```

**Notes & troubleshooting**
- Ensure network access to the XMPP server used by SPADE. If the agent cannot connect, verify server availability and credentials.
- `fire_type` is set to `"none"` when severity is `"none"` (no active fire).
- `casualties` is only non-zero for `high` and `critical` severity events.

**Deliverables**
- Environment setup confirmation and working `sensor_agent.py` that generates fire incident percepts consumed by downstream labs.