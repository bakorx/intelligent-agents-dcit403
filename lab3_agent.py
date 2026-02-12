"""Lab 3: FSM-based reactive agent.

Watches `event_logs.txt` for new sensor reports and runs a small FSM
to demonstrate goal-driven reactive behavior.

Usage:
    python lab3_agent.py

The script logs state transitions to stdout and to `lab3_execution.txt`.
"""
import time
import ast
from enum import Enum
from datetime import datetime
from typing import Dict

EVENT_LOG = "event_logs.txt"
TRACE_LOG = "lab3_execution.txt"
POLL_INTERVAL = 1.0


class State(Enum):
    IDLE = "IDLE"
    ALERT = "ALERT"
    RESPONDING = "RESPONDING"
    RESCUING = "RESCUING"
    RECOVERING = "RECOVERING"


class FSMAgent:
    def __init__(self):
        self.state = State.IDLE
        self._write_trace(f"{self._ts()} START state={self.state.value}")

    def _ts(self):
        return datetime.utcnow().isoformat() + "Z"

    def _write_trace(self, msg: str):
        print(msg)
        with open(TRACE_LOG, "a") as f:
            f.write(msg + "\n")

    def transition(self, new_state: State, reason: str = ""):
        old = self.state
        self.state = new_state
        self._write_trace(f"{self._ts()} TRANSITION {old.value} -> {new_state.value} : {reason}")

    def handle_event(self, event: Dict):
        sev = event.get("severity", "none")
        damage = int(event.get("damage", 0))
        reason = f"event(severity={sev},damage={damage})"

        if self.state == State.IDLE:
            if sev != "none":
                self.transition(State.ALERT, reason)
                self._decide_response(event)

        elif self.state == State.ALERT:
            # already investigating; decide if escalate
            self._decide_response(event)

        elif self.state == State.RESPONDING:
            # simulate arrival if damage large or severity high
            if sev in ("high", "critical") or damage > 50:
                self.transition(State.RESCUING, "arrived_on_scene")
            else:
                self.transition(State.IDLE, "false_alarm_or_low_priority")

        elif self.state == State.RESCUING:
            # simulate rescue completion condition
            if damage <= 20:
                self.transition(State.RECOVERING, "rescue_complete_low_damage")
            else:
                # reduce damage to simulate progress
                new_damage = max(0, damage - 30)
                self._write_trace(f"{self._ts()} ACTION: performing_rescue -> damage now {new_damage}")
                if new_damage <= 20:
                    self.transition(State.RECOVERING, "rescue_complete")
                else:
                    # stay rescuing
                    pass

        elif self.state == State.RECOVERING:
            self.transition(State.IDLE, "mission_closed")

    def _decide_response(self, event: Dict):
        sev = event.get("severity", "none")
        damage = int(event.get("damage", 0))
        if sev in ("critical", "high") or damage > 60:
            self.transition(State.RESPONDING, "allocate_rapid_response")
        elif sev in ("medium",) or damage > 20:
            self.transition(State.RESPONDING, "allocate_standard_response")
        else:
            self.transition(State.IDLE, "monitor_only")


def follow_file(path: str):
    """Generator yielding new lines appended to a file (like tail -f)."""
    try:
        with open(path, "r") as f:
            # go to start (process existing lines) - this lab expects trigger on lines
            while True:
                line = f.readline()
                if not line:
                    break
                yield line.rstrip("\n")

        with open(path, "r") as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    yield line.rstrip("\n")
                else:
                    time.sleep(POLL_INTERVAL)
    except FileNotFoundError:
        # If the file does not yet exist, create it and yield nothing
        open(path, "a").close()
        return


def parse_event(line: str):
    try:
        # sensor_agent writes Python dict repr() strings; use ast.literal_eval to parse
        return ast.literal_eval(line.strip())
    except Exception:
        return {}


def main():
    agent = FSMAgent()
    # clear trace log
    open(TRACE_LOG, "w").close()
    agent._write_trace(f"{agent._ts()} LAB3_AGENT_STARTED")

    for raw in follow_file(EVENT_LOG):
        if not raw:
            continue
        event = parse_event(raw)
        if not event:
            agent._write_trace(f"{agent._ts()} WARNING: could not parse line: {raw}")
            continue
        agent._write_trace(f"{agent._ts()} OBSERVED {event}")
        agent.handle_event(event)


if __name__ == "__main__":
    main()
