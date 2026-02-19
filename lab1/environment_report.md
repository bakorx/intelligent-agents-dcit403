Environment setup report (Lab 1)

System: GitHub Codespaces (Ubuntu container)

Python: Use the workspace Python (3.x) provided by Codespaces. Verify with `python --version`.

SPADE: Install with `pip install -r requirements.txt` which contains `spade`.

XMPP server: I used the provided online XMPP server; credentials used in examples:
- JID: agentbakor@xmpp.jp
- Password: bakoragent

Agent execution: Run `python sensor_agent.py` to start the SensorAgent. The agent periodically logs simulated disaster percepts to `event_logs.txt` and stdout.

Notes:
- Ensure network access to the XMPP server from Codespaces.
- If SPADE cannot connect, check server availability and credentials.
