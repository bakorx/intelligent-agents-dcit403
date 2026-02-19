# Lab 4 — Agent Communication using FIPA-ACL

**Objective**
- Enable inter-agent communication using FIPA-ACL performatives and show how messages trigger actions.

**Background**
- Multi-agent coordination relies on standardized message exchange. FIPA-ACL defines performatives such as `REQUEST` and `INFORM` that structure interactions between agents.
- This lab demonstrates a minimal Coordinator/Responder pair implemented with SPADE that exchange ACL messages and log message events and actions.

**Design & Roles**
- **CoordinatorAgent**: Initiates a `REQUEST` containing an event (timestamp, severity, damage) asking the Responder to handle it.
- **ResponderAgent**: Listens for incoming messages, parses `REQUEST` messages, performs a simulated action (logs handling), and replies with an `INFORM` acknowledging completion.

**Files**
- Code: [comm_agents.py](comm_agents.py#L1)
- Sample logs: [message_logs.txt](message_logs.txt#L1)

**Implementation details**
- The code uses SPADE's `Message` class and message metadata to set the performative (`request` / `inform`).
- `CoordinatorAgent` behaviour:
  - `SendRequestBehaviour` (one-shot): constructs an event dict and sends it as a `REQUEST` to the responder; logs the outgoing message to `message_logs.txt`.
  - `ReceiveInformBehaviour` (cyclic): listens for `INFORM` replies and logs them.
- `ResponderAgent` behaviour:
  - `ReceiveBehaviour` (cyclic): receives messages, checks `performative` metadata, parses the body (using `ast.literal_eval` when appropriate), logs the incoming message and a simulated action, then replies with an `INFORM` containing a small status dict.

**Message format**
- Metadata: `performative` string set in `msg.metadata` (e.g., `request` or `inform`).
- Body: Python dict representation (string) containing event details or status responses.

**Sample message log (excerpt)**
- See full sample in [message_logs.txt](message_logs.txt#L1). Example entries:
  - `SENT to responder@xmpp.jp performative=request body={...}`
  - `RECEIVED from responder@xmpp.jp performative=inform body={"status":"processed",...}`

**How messages trigger actions**
- On receiving a `REQUEST` performative, the Responder:
  - Parses the request body as an event.
  - Logs `ACTION: handling_event` to show the work performed.
  - Sends an `INFORM` reply with processing status.
- The Coordinator logs the sent request and the received inform, forming a complete request/response trace useful for audit and debugging.

**How to run (quick)**
1. Install dependencies:
```bash
python -m pip install -r requirements.txt
```
2. Run the demo (replace JIDs/passwords with valid XMPP accounts reachable from your environment):
```bash
python comm_agents.py --coordinator-jid coordinator@xmpp.jp --coordinator-pass coordpwd \
  --responder-jid responder@xmpp.jp --responder-pass respwd --runtime 15
```
3. Inspect logs while running:
```bash
tail -f message_logs.txt
```

**Limitations & notes**
- The demo uses plain string bodies containing Python `dict` reprs; in production use structured formats (JSON) and proper ontology/ontology mapping.
- The example assumes accessible XMPP accounts. If an XMPP server is not available, the code still documents the approach and sample logs provide expected behaviour.

**Possible extensions**
- Use JSON or ACL content language headers instead of Python reprs.
- Add error handling, retries, timeout-based re-requests, and richer performatives (e.g., `CFP`, `PROPOSE`).
- Integrate with the FSM agent from Lab 3: the Coordinator could forward sensor events as `REQUEST`s to specialized responders.

Prepared on: 2026-02-12
