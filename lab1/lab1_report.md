# Lab 1 — Basic Agent Behaviour and Periodic Actions

**Objective**
- Implement and verify a simple SPADE agent that performs periodic behaviour to demonstrate agent lifecycle and behaviours, in the context of a fire disaster monitoring system.

**Summary**
- `basic_agent.py` contains `BasicAgent`, a minimal SPADE agent with a `GreetingBehaviour` (a `CyclicBehaviour`) that prints a fire monitoring status message periodically.
- The code demonstrates agent setup, adding behaviours, starting/stopping an agent, and using asynchronous behaviour with `asyncio`.

**Key design points**
- `GreetingBehaviour` is a `CyclicBehaviour` that executes repeatedly, printing a fire system status message, then sleeping between iterations — demonstrating recurring monitoring tasks.
- `BasicAgent.setup()` registers behaviours when the agent starts.
- The file includes a `main()` runner that accepts command-line arguments for JID, password, and auto-registration.

**How to run**
1. Install dependencies:
```bash
/bin/python3 -m pip install spade --break-system-packages
```
2. Run the basic agent:
```bash
python3 basic_agent.py --jid agentbakor@xmpp.jp --password bakoragent
```

**Observations**
- This lab demonstrates how to implement simple agent behaviours and the SPADE lifecycle. It forms the foundation for the fire response labs that follow, which add event-driven FSM logic and inter-agent communication.

**Next steps**
- Extend the basic agent to monitor fire sensor events from `event_logs.txt`, integrate with the fire sensor agent, or convert the cyclic behaviour to a `PeriodicBehaviour` for more precise monitoring intervals.