#!/bin/bash
set -e
cd "$(dirname "$0")"
python -m pip install -r requirements.txt
# Run agent in background and capture output
nohup python sensor_agent.py > agent_output.log 2>&1 &
echo $! > agent.pid
echo "Agent started, PID=$(cat agent.pid)"
