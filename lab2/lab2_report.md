# Lab 1 — Environment and Agent Platform Setup

**Objective**
- Set up the development environment and verify a minimal SPADE-based sensor agent runs and logs percepts.

**Environment**
- Platform: GitHub Codespaces (Ubuntu container). Use the workspace Python (`python --version`) provided by Codespaces.
- Dependencies: Install with:
```bash
python -m pip install -r requirements.txt
```
- SPADE: Listed in `requirements.txt` and used for agent scaffolding.
- XMPP credentials used in examples:
  - JID: agentbakor@xmpp.jp
  - Password: bakoragent

**Provided files & purpose**
- `sensor_agent.py`: A SPADE `SensorAgent` that periodically generates simulated disaster percepts (dicts with `timestamp`, `severity`, `damage`) and appends them to `event_logs.txt`.
- `run_agent.sh`: Helper to run the agent in background and redirect logs (see repository root).
- `event_logs.txt`: Accumulated sensor percepts (created by the sensor agent).

**How to run**
1. Install requirements:
```bash
python -m pip install -r requirements.txt
```
2. Start the sensor agent (period default 5s):
```bash
python sensor_agent.py --period 2
```
3. Tail the logs:
```bash
tail -f event_logs.txt
```

**Notes & troubleshooting**
- Ensure network access to the XMPP server used by SPADE. If the agent cannot connect, verify server availability and credentials.
- If running locally without an XMPP server, the agent behaviour can still be inspected by running modified code that writes sample lines to `event_logs.txt`.

**Deliverables**
- Environment setup confirmation and working `sensor_agent.py` that generates percepts consumed by downstream labs.
