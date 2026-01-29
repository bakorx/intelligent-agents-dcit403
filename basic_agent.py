import asyncio
import argparse
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class BasicAgent(Agent):
    """A basic SPADE agent that prints a message periodically"""
    
    class GreetingBehaviour(CyclicBehaviour):
        """A cyclic behaviour that runs repeatedly"""
        
        async def run(self):
            print(f"{self.agent.name}: Hello! I'm a basic SPADE agent.")
            await asyncio.sleep(2)
    
    async def setup(self):
        """Called when the agent starts"""
        print(f"Agent {self.name} starting up...")
        behaviour = self.GreetingBehaviour()
        self.add_behaviour(behaviour)


async def main():
    """Main function to run the agent"""
    parser = argparse.ArgumentParser(description="Run BasicAgent with provided XMPP credentials")
    parser.add_argument("--jid", default="agentbakor@xmpp.jp", help="Agent JID (default: agentbakor@xmpp.jp)")
    parser.add_argument("--password", default="bakoragent", help="Agent password (default: bakoragent)")
    parser.add_argument("--auto-register", dest="auto_register", action="store_true", help="Attempt to auto-register the agent on the XMPP server")
    args = parser.parse_args()

    agent = BasicAgent(args.jid, args.password)

    try:
        await agent.start(auto_register=args.auto_register)
        print("Agent started successfully!")

        # Keep the agent running for 10 seconds
        await asyncio.sleep(10)

    finally:
        await agent.stop()
        print("Agent stopped.")


if __name__ == "__main__":
    asyncio.run(main())