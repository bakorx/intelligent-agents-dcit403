"""Lab 4 — Agent communication using FIPA-ACL (SPADE) — Fire Disaster

CoordinatorAgent sends a REQUEST containing a fire incident event to the
ResponderAgent. The Responder parses the message, performs a simulated
fire-handling action, logs it to message_logs.txt, and replies with an
INFORM acknowledgement.

Usage (requires XMPP server access and valid credentials):
    python comm_agents.py --coordinator-jid agentbakor@xmpp.jp --coordinator-pass bakoragent \
        --responder-jid agentbakor@xmpp.jp --responder-pass bakoragent --auto-register
"""
import argparse
import asyncio
import ast
import time
import re
from datetime import datetime, timezone

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message

LOG_FILE = "message_logs.txt"

FIRE_RESPONSE_ACTIONS = {
    "structural": "deploy_ladder_truck_and_hose_team",
    "wildfire":   "dispatch_aerial_support_and_ground_crew",
    "electrical": "isolate_power_and_deploy_co2_units",
    "chemical":   "activate_hazmat_team_and_foam_suppression",
    "vehicle":    "deploy_dry_powder_units",
    "none":       "stand_down_units",
}


def ts():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ResponderAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                perf = msg.metadata.get("performative", "")
                content = msg.body or ""

                with open(LOG_FILE, "a") as f:
                    f.write(f"{ts()} RECEIVED from {str(msg.sender)} performative={perf} body={content}\n")

                if perf.lower() == "request":
                    try:
                        event = ast.literal_eval(content)
                    except Exception:
                        event = {"raw": content}

                    fire_type = event.get("fire_type", "none")
                    location = event.get("location", "unknown")
                    spread_rate = event.get("spread_rate", 0.0)
                    casualties = event.get("casualties", 0)
                    action = FIRE_RESPONSE_ACTIONS.get(fire_type, "deploy_general_fire_units")

                    with open(LOG_FILE, "a") as f:
                        f.write(
                            f"{ts()} ACTION: {action} | "
                            f"fire_type={fire_type}, location={location}, "
                            f"spread_rate={spread_rate}m/min, casualties={casualties}\n"
                        )

                    reply = Message(to=str(msg.sender))
                    reply.set_metadata("performative", "inform")
                    reply.body = str({
                        "status": "processed",
                        "action_taken": action,
                        "location": location,
                        "timestamp": ts(),
                    })
                    await self.send(reply)

    async def setup(self):
        self.add_behaviour(self.ReceiveBehaviour())


class CoordinatorAgent(Agent):
    class SendRequestBehaviour(OneShotBehaviour):
        async def run(self):
            # Build a sample fire incident event
            event = {
                "timestamp": ts(),
                "severity": "high",
                "damage": 75,
                "fire_type": "structural",
                "location": "Block B",
                "spread_rate": 6.3,
                "casualties": 4,
            }
            msg = Message(to=self.agent.responder_jid)
            msg.set_metadata("performative", "request")
            msg.body = str(event)
            await self.send(msg)

            with open(LOG_FILE, "a") as f:
                f.write(f"{ts()} SENT to {self.agent.responder_jid} performative=request body={event}\n")

    class ReceiveInformBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=5)
            if msg:
                perf = msg.metadata.get("performative", "")
                with open(LOG_FILE, "a") as f:
                    f.write(f"{ts()} RECEIVED from {str(msg.sender)} performative={perf} body={msg.body}\n")

    def __init__(self, jid, password, responder_jid):
        super().__init__(jid, password)
        self.responder_jid = responder_jid

    async def setup(self):
        self.add_behaviour(self.SendRequestBehaviour())
        self.add_behaviour(self.ReceiveInformBehaviour())


async def run_agents(coord_jid, coord_pwd, resp_jid, resp_pwd, runtime=10, auto_register=False):
    coord = CoordinatorAgent(coord_jid, coord_pwd, responder_jid=resp_jid)
    resp = ResponderAgent(resp_jid, resp_pwd)

    await resp.start(auto_register=auto_register)
    await coord.start(auto_register=auto_register)

    try:
        await asyncio.sleep(runtime)
    finally:
        await coord.stop()
        await resp.stop()


def main():
    parser = argparse.ArgumentParser(description="Run fire coordinator and responder agents (SPADE)")
    parser.add_argument("--coordinator-jid", default="agentbakor@xmpp.jp")
    parser.add_argument("--coordinator-pass", default="bakoragent")
    parser.add_argument("--responder-jid", default="agentbakor@xmpp.jp")
    parser.add_argument("--responder-pass", default="bakoragent")
    parser.add_argument("--runtime", type=int, default=10)
    parser.add_argument("--auto-register", action="store_true")
    args = parser.parse_args()

    open(LOG_FILE, "a").close()

    asyncio.run(run_agents(
        args.coordinator_jid, args.coordinator_pass,
        args.responder_jid, args.responder_pass,
        runtime=args.runtime, auto_register=args.auto_register,
    ))


if __name__ == "__main__":
    main()