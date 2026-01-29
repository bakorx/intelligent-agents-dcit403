# Lab 1 — Environment and Agent Platform Setup

This repo contains a minimal SPADE SensorAgent for the lab.

Files:
- `sensor_agent.py`: basic SPADE agent that periodically logs simulated disaster percepts.
- `requirements.txt`: dependencies (spade).
- `environment_report.md`: short environment setup report.
- `run_agent.sh`: helper to run the agent in background and capture logs.

Quick start (in Codespaces):
```bash
python -m pip install -r requirements.txt
./run_agent.sh
tail -f agent_output.log
```

Default credentials used by the agent:
- JID: agentbakor@xmpp.jp
- Password: bakoragent

To capture a screenshot in Codespaces: open the terminal running the agent, ensure logs are visible, then use the Codespaces UI `Capture Screenshot` or take a screenshot with your OS tools. Save it to the repo before submission.
# intelligent-agents-dcit403
Laboratory exercises and practical implementations  – Designing Intelligent Agents, using Python and the SPADE framework to develop multi-agent systems for disaster response and coordination.
