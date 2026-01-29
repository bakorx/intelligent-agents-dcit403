import asyncio
import logging
import random
import time
from datetime import datetime
import argparse

from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sensor_agent")


class SensorAgent(Agent):
    class SenseBehaviour(PeriodicBehaviour):
        async def run(self):
            ts = datetime.utcnow().isoformat() + "Z"
            severity = random.choice(["none", "low", "medium", "high", "critical"])
            damage = random.randint(0, 100)
            event = {"timestamp": ts, "severity": severity, "damage": damage}
            # Log to console and append to file
            logger.info(f"Percept: {event}")
            with open("event_logs.txt", "a") as f:
                f.write(f"{event}\n")

    async def setup(self):
        logger.info(f"{self.name} starting setup")
        b = self.SenseBehaviour(period=self.behaviour_period)
        self.add_behaviour(b)

    def __init__(self, jid, password, behaviour_period=5):
        super().__init__(jid, password)
        # store period for behaviour creation inside setup
        self.behaviour_period = behaviour_period


def main():
    parser = argparse.ArgumentParser(description="Run SensorAgent (SPADE)")
    parser.add_argument("--jid", default="agentbakor@xmpp.jp", help="Agent JID")
    parser.add_argument("--password", default="bakoragent", help="Agent password")
    parser.add_argument("--period", type=int, default=5, help="Behaviour period (seconds)")
    args = parser.parse_args()

    agent = SensorAgent(args.jid, args.password, behaviour_period=args.period)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(agent.start())
    except Exception as e:
        logger.error("Agent failed to start: %s", e)
        return

    logger.info("Agent started. Press Ctrl+C to stop.")
    try:
        while agent.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received: stopping agent")
    finally:
        try:
            loop.run_until_complete(agent.stop())
        except Exception:
            agent.stop()
        time.sleep(1)


if __name__ == "__main__":
    main()
