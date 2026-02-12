"""Lab 4 — Agent communication using FIPA-ACL (SPADE)

This module contains two simple SPADE agents demonstrating ACL message
exchange using `REQUEST` and `INFORM` performatives. The CoordinatorAgent
sends a `REQUEST` to the ResponderAgent; the Responder parses the message,
performs a simulated action (writes to `message_logs.txt`) and replies with
an `INFORM` acknowledgement.

Usage (example, requires XMPP server access and valid credentials):
    python comm_agents.py --coordinator-jid coord@xmpp.jp --coordinator-pass pwd \
        --responder-jid responder@xmpp.jp --responder-pass pwd

If you do not have an XMPP server available, you can still inspect the code
and the sample `message_logs.txt` included in the repo.
"""
import argparse
import asyncio
import ast
import time
import re
from datetime import datetime

from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message

LOG_FILE = "message_logs.txt"


def ts():
    return datetime.utcnow().isoformat() + "Z"


class ResponderAgent(Agent):
    class ReceiveBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=1)
            if msg:
                perf = msg.metadata.get("performative", "")
                content = msg.body or ""
                # log incoming message
                with open(LOG_FILE, "a") as f:
                    f.write(f"{ts()} RECEIVED from {str(msg.sender)} performative={perf} body={content}\n")

                # handle REQUEST performative
                if perf.lower() == "request":
                    # parse body if it's a dict repr
                    try:
                        event = ast.literal_eval(content)
                    except Exception:
                        event = {"raw": content}

                    # Simulate action: write event handling to log
                    with open(LOG_FILE, "a") as f:
                        f.write(f"{ts()} ACTION: handling_event {event}\n")

                    # reply with INFORM to confirm action
                    reply = Message(to=str(msg.sender))
                    reply.set_metadata("performative", "inform")
                    reply.body = str({"status": "processed", "timestamp": ts()})
                    await self.send(reply)

    async def setup(self):
        self.add_behaviour(self.ReceiveBehaviour())


class CoordinatorAgent(Agent):
    class SendRequestBehaviour(OneShotBehaviour):
        async def run(self):
            # build a sample event and send as REQUEST
            event = {"timestamp": ts(), "severity": "high", "damage": 75}
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
        # send a single request shortly after startup
        self.add_behaviour(self.SendRequestBehaviour())
        # listen for INFORM responses
        self.add_behaviour(self.ReceiveInformBehaviour())


async def run_agents(coord_jid, coord_pwd, resp_jid, resp_pwd, runtime=10):
    coord = CoordinatorAgent(coord_jid, coord_pwd, responder_jid=resp_jid)
    resp = ResponderAgent(resp_jid, resp_pwd)

    await resp.start()
    await coord.start()

    try:
        await asyncio.sleep(runtime)
    finally:
        await coord.stop()
        await resp.stop()


def main():
    # Attempt to read default credentials from basic_agent.py if present
    basic_jid = None
    basic_pass = None
    try:
        with open("basic_agent.py", "r") as bf:
            content = bf.read()
            m_jid = re.search(r"add_argument\(\"--jid\",\s*default=\"([^\"]+)\"", content)
            m_pw = re.search(r"add_argument\(\"--password\",\s*default=\"([^\"]+)\"", content)
            if m_jid:
                basic_jid = m_jid.group(1)
            if m_pw:
                basic_pass = m_pw.group(1)
    except FileNotFoundError:
        pass

    parser = argparse.ArgumentParser(description="Run coordinator and responder agents (SPADE)")
    parser.add_argument("--coordinator-jid", default=(basic_jid or "coordinator@xmpp.jp"), help="Coordinator JID")
    parser.add_argument("--coordinator-pass", default=(basic_pass or "coordpass"), help="Coordinator password")
    parser.add_argument("--responder-jid", default=(basic_jid or "responder@xmpp.jp"), help="Responder JID")
    parser.add_argument("--responder-pass", default=(basic_pass or "responderpass"), help="Responder password")
    parser.add_argument("--runtime", type=int, default=10, help="Seconds to run the demo agents")
    args = parser.parse_args()

    # ensure log file exists
    open(LOG_FILE, "a").close()

    asyncio.run(run_agents(args.coordinator_jid, args.coordinator_pass, args.responder_jid, args.responder_pass, runtime=args.runtime))


if __name__ == "__main__":
    main()
