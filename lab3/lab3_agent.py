"""Lab 3 — Goals, Events, and Reactive Behavior

This module implements a reactive agent using a Finite State Machine (FSM) to handle
disaster response scenarios. The agent monitors `event_logs.txt` for sensor reports,
transitions between states based on event severity and response actions, and logs
its execution trace to `lab3_execution.txt`.

FSM States:
- IDLE: Waiting for events
- ALERT: Event detected, assessing
- RESPONDING: Resources allocated, moving to scene
- RESCUING: On scene, performing rescue
- RECOVERING: Rescue complete, recovering

Transitions triggered by sensor events and simulated actions.
"""
import asyncio
import time
import ast
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

LOG_FILE = "../lab2/event_logs.txt"
EXECUTION_LOG = "lab3_execution.txt"

def ts():
    return datetime.utcnow().isoformat() + "Z"

class ReactiveAgent(Agent):
    class FSMBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.state = "IDLE"
            self.last_event_time = None
            self.current_event = None

        async def run(self):
            # Read latest event from log
            try:
                with open(LOG_FILE, "r") as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line:
                            try:
                                event = ast.literal_eval(last_line.split(" - ")[-1])
                                event_time = last_line.split(" - ")[0]
                                if event_time != self.last_event_time:
                                    self.last_event_time = event_time
                                    self.current_event = event
                                    await self.handle_event(event)
                            except (ValueError, IndexError, SyntaxError):
                                pass
            except FileNotFoundError:
                pass

            # Simulate state transitions and actions
            await self.perform_actions()

            await asyncio.sleep(1)  # Check every second

        async def handle_event(self, event):
            severity = event.get("severity", "none")
            with open(EXECUTION_LOG, "a") as f:
                f.write(f"{ts()} EVENT: {event}\n")

            if self.state == "IDLE" and severity != "none":
                self.state = "ALERT"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(f"{ts()} STATE: IDLE -> ALERT (new_event)\n")
            elif self.state == "ALERT":
                # Simulate allocate_resources
                await asyncio.sleep(0.5)
                self.state = "RESPONDING"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(f"{ts()} STATE: ALERT -> RESPONDING (allocate_resources)\n")
            elif self.state == "RESPONDING":
                # Simulate arrive_on_scene
                await asyncio.sleep(0.5)
                self.state = "RESCUING"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(f"{ts()} STATE: RESPONDING -> RESCUING (arrive_on_scene)\n")
            elif self.state == "RESCUING":
                # Simulate rescue_complete
                await asyncio.sleep(0.5)
                self.state = "RECOVERING"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(f"{ts()} STATE: RESCUING -> RECOVERING (rescue_complete)\n")
            elif self.state == "RECOVERING":
                # Simulate mission_closed
                await asyncio.sleep(0.5)
                self.state = "IDLE"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(f"{ts()} STATE: RECOVERING -> IDLE (mission_closed)\n")

        async def perform_actions(self):
            # Additional actions based on state
            if self.state == "ALERT":
                print(f"{ts()} Agent assessing situation...")
            elif self.state == "RESPONDING":
                print(f"{ts()} Agent allocating resources and responding...")
            elif self.state == "RESCUING":
                print(f"{ts()} Agent performing rescue operations...")
            elif self.state == "RECOVERING":
                print(f"{ts()} Agent recovering and closing mission...")

    async def setup(self):
        print(f"Reactive Agent {self.name} starting...")
        fsm_behaviour = self.FSMBehaviour()
        self.add_behaviour(fsm_behaviour)


async def main():
    # For simplicity, run without XMPP for this demo
    # In a full setup, this would be a SPADE agent with JID
    agent = ReactiveAgent("reactive@localhost", "password")  # Dummy credentials
    try:
        # Skip start for demo, just run the behaviour
        await agent.setup()
        behaviour = agent.behaviours[0]
        # Run for 30 seconds
        start_time = time.time()
        while time.time() - start_time < 30:
            await behaviour.run()
        print("Demo completed. Check lab3_execution.txt for trace.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())