# Lab 4 — Agent Communication using FIPA-ACL (Fire Disaster)

**Objective**
- Enable inter-agent communication using FIPA-ACL performatives and show how fire incident messages trigger specific response actions.

**Background**
- Multi-agent fire response coordination relies on standardized message exchange. FIPA-ACL defines performatives such as `REQUEST` and `INFORM` that structure interactions between agents.
- This lab demonstrates a Coordinator/Responder pair implemented with SPADE that exchange fire incident ACL messages, select the appropriate fire-fighting action based on fire type, and log all events.

**Design & Roles**
- **CoordinatorAgent**: Detects a fire incident and sends a `REQUEST` containing the full fire event (timestamp, severity, damage, fire_type, location, spread_rate, casualties) to the Responder.
- **ResponderAgent**: Listens for incoming `REQUEST` messages, parses the fire event, looks up the correct fire-fighting action based on `fire_type`, logs the action, and replies with an `INFORM` acknowledging completion.

**Fire Type → Action Mapping**
| `fire_type` | Action Dispatched |
|---|---|
| `structural` | `deploy_ladder_truck_and_hose_team` |
| `wildfire` | `dispatch_aerial_support_and_ground_crew` |
| `electrical` | `isolate_power_and_deploy_co2_units` |
| `chemical` | `activate_hazmat_team_and_foam_suppression` |
| `vehicle` | `deploy_dry_powder_units` |
| `none` | `stand_down_units` |

**Files**
- Code: [comm_agents.py](comm_agents.py)
- Sample logs: [message_logs.txt](message_logs.txt)

**Implementation details**
- The code uses SPADE's `Message` class and message metadata to set the performative (`request` / `inform`).
- `CoordinatorAgent` behaviours:
  - `SendRequestBehaviour` (one-shot): constructs a fire incident event dict and sends it as a `REQUEST` to the responder; logs the outgoing message to `message_logs.txt`.
  - `ReceiveInformBehaviour` (cyclic): listens for `INFORM` replies and logs them.
- `ResponderAgent` behaviour:
  - `ReceiveBehaviour` (cyclic): receives messages, checks `performative` metadata, parses the body using `ast.literal_eval`, looks up the fire-fighting action from `FIRE_RESPONSE_ACTIONS`, logs the action with full fire context, then replies with an `INFORM` containing status, action taken, and location.

**Message format**
- Metadata: `performative` string (`request` or `inform`).
- Request body: fire event dict — `timestamp`, `severity`, `damage`, `fire_type`, `location`, `spread_rate`, `casualties`.
- Inform body: response dict — `status`, `action_taken`, `location`, `timestamp`.

**Sample message log (excerpt)**
```
SENT to agentbakor@xmpp.jp performative=request body={'severity': 'high', 'damage': 75, 'fire_type': 'structural', 'location': 'Block B', 'spread_rate': 6.3, 'casualties': 4}
RECEIVED from agentbakor@xmpp.jp performative=request body={...}
ACTION: deploy_ladder_truck_and_hose_team | fire_type=structural, location=Block B, spread_rate=6.3m/min, casualties=4
RECEIVED from agentbakor@xmpp.jp performative=inform body={'status': 'processed', 'action_taken': 'deploy_ladder_truck_and_hose_team', 'location': 'Block B', ...}
```

**How messages trigger actions**
- On receiving a `REQUEST` performative, the Responder:
  1. Parses the fire event body.
  2. Looks up `fire_type` in `FIRE_RESPONSE_ACTIONS` to determine the correct response.
  3. Logs `ACTION: <action> | fire_type=..., location=..., spread_rate=..., casualties=...`.
  4. Sends an `INFORM` reply with the action taken and location.
- The Coordinator logs the sent request and the received inform, forming a complete fire incident request/response trace.

**How to run (quick)**
1. Install dependencies:
```bash
/bin/python3 -m pip install spade --break-system-packages
```
2. Run the demo:
```bash
python3 comm_agents.py --coordinator-jid agentbakor@xmpp.jp --coordinator-pass bakoragent \
  --responder-jid agentbakor@xmpp.jp --responder-pass bakoragent --runtime 15
```
3. Inspect logs while running:
```bash
tail -f message_logs.txt
```

**Possible extensions**
- Feed real fire events from `event_logs.txt` into the Coordinator instead of a hardcoded event.
- Add more performatives: `CFP` (call for proposals) to negotiate which fire unit responds, or `PROPOSE` for resource bidding.
- Integrate with the Lab 3 FSM agent: the Coordinator forwards sensor fire events as `REQUEST`s to specialized responders based on fire type.
- Use JSON bodies instead of Python dict string representations for better interoperability.

---
Prepared on: 2026-02-26