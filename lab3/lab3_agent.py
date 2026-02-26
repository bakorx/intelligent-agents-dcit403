"""Lab 3 — Goals, Events, and Reactive Behavior (Fire Disaster)

FSM States:
- IDLE:        Monitoring — no active fire incident
- ALERT:       Fire signal detected, assessing fire type and spread rate
- RESPONDING:  Fire units dispatched, en route to location
- SUPPRESSING: On scene, actively suppressing the fire
- RECOVERING:  Fire contained, site safety check and handover

Transitions triggered by fire sensor events from event_logs.txt.
All state transitions and actions are logged to lab3_execution.txt.
"""
import asyncio
import time
import ast
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

LOG_FILE = "../lab2/event_logs.txt"
EXECUTION_LOG = "lab3_execution.txt"

# Thresholds for fire response decisions
HIGH_SPREAD_THRESHOLD = 5.0    # metres per minute — triggers rapid response
CRITICAL_DAMAGE_THRESHOLD = 70  # damage value — escalates to full suppression mode


def ts():
    return datetime.utcnow().isoformat() + "Z"


class FireResponseAgent(Agent):
    class FSMBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.state = "IDLE"
            self.last_event_time = None
            self.current_event = None

        async def run(self):
            # Read latest fire event from log
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

            await self.perform_actions()
            await asyncio.sleep(1)

        async def handle_event(self, event):
            severity = event.get("severity", "none")
            fire_type = event.get("fire_type", "unknown")
            spread_rate = event.get("spread_rate", 0.0)
            damage = event.get("damage", 0)
            location = event.get("location", "unknown")
            casualties = event.get("casualties", 0)

            with open(EXECUTION_LOG, "a") as f:
                f.write(f"{ts()} EVENT: {event}\n")

            if self.state == "IDLE" and severity != "none":
                self.state = "ALERT"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(
                        f"{ts()} STATE: IDLE -> ALERT "
                        f"(fire_detected | type={fire_type}, location={location}, "
                        f"spread_rate={spread_rate}m/min)\n"
                    )

            elif self.state == "ALERT":
                # Decide response level based on spread rate and damage
                await asyncio.sleep(0.5)
                if spread_rate >= HIGH_SPREAD_THRESHOLD or damage >= CRITICAL_DAMAGE_THRESHOLD:
                    response = "dispatch_rapid_fire_units"
                else:
                    response = "dispatch_standard_fire_units"
                self.state = "RESPONDING"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(
                        f"{ts()} STATE: ALERT -> RESPONDING "
                        f"({response} | casualties={casualties})\n"
                    )

            elif self.state == "RESPONDING":
                # Simulate units arriving on scene
                await asyncio.sleep(0.5)
                self.state = "SUPPRESSING"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(
                        f"{ts()} STATE: RESPONDING -> SUPPRESSING "
                        f"(units_arrived_on_scene | fire_type={fire_type})\n"
                    )

            elif self.state == "SUPPRESSING":
                # Simulate fire suppression reducing damage
                suppressed_damage = max(0, damage - random_suppression())
                await asyncio.sleep(0.5)
                self.state = "RECOVERING"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(
                        f"{ts()} STATE: SUPPRESSING -> RECOVERING "
                        f"(fire_contained | damage reduced to {suppressed_damage})\n"
                    )

            elif self.state == "RECOVERING":
                # Site safety check and mission closure
                await asyncio.sleep(0.5)
                self.state = "IDLE"
                with open(EXECUTION_LOG, "a") as f:
                    f.write(
                        f"{ts()} STATE: RECOVERING -> IDLE "
                        f"(site_cleared | mission_closed)\n"
                    )

        async def perform_actions(self):
            if self.state == "ALERT":
                print(f"{ts()} [ALERT] Assessing fire type, location, and spread rate...")
            elif self.state == "RESPONDING":
                print(f"{ts()} [RESPONDING] Fire units en route to scene...")
            elif self.state == "SUPPRESSING":
                print(f"{ts()} [SUPPRESSING] Actively suppressing fire, monitoring spread...")
            elif self.state == "RECOVERING":
                print(f"{ts()} [RECOVERING] Fire contained — site safety check in progress...")

    async def setup(self):
        print(f"Fire Response Agent {self.name} starting...")
        fsm_behaviour = self.FSMBehaviour()
        self.add_behaviour(fsm_behaviour)


def random_suppression():
    """Simulate damage reduction from fire suppression activity."""
    import random
    return random.randint(20, 60)


async def main():
    agent = FireResponseAgent("fire_response@localhost", "password")
    try:
        await agent.setup()
        behaviour = agent.behaviours[0]
        start_time = time.time()
        while time.time() - start_time < 30:
            await behaviour.run()
        print("Demo completed. Check lab3_execution.txt for trace.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())