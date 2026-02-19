# Lab 2 — Basic Agent Behaviour and Periodic Actions

**Objective**
- Implement and verify a simple SPADE agent that performs periodic behaviour to demonstrate agent lifecycle and behaviours.

**Summary**
- `basic_agent.py` contains `BasicAgent`, a minimal SPADE agent with a `GreetingBehaviour` (a `CyclicBehaviour`) that prints a greeting periodically.
- The code demonstrates agent setup, adding behaviours, starting/stopping an agent, and using asynchronous behaviour with `asyncio`.

**Key design points**
- `GreetingBehaviour` is a `CyclicBehaviour` that executes repeatedly and sleeps between iterations, demonstrating recurring tasks.
- `BasicAgent.setup()` registers behaviours when the agent starts.
- The file also includes a `main()` runner that accepts command-line arguments for JID, password, and auto-registration.

**How to run**
1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```
2. Run the basic agent (uses example credentials in README):
```bash
python basic_agent.py --jid agentbakor@xmpp.jp --password bakoragent
```

**Observations**
- This lab demonstrates how to implement simple agent behaviours and the SPADE lifecycle. It forms a foundation for later labs that add event-driven or goal-directed logic.

**Next steps**
- Extend the basic agent to handle messages, integrate with the sensor agent, or convert the cyclic behaviour to a `PeriodicBehaviour` for more precise timing.
