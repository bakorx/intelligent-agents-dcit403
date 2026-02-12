# Lab 3 — Goals, Events, and Reactive Behavior

**Objective**
- Model agent goals and event-triggered reactive behavior using a finite state machine (FSM).

**Background**
- The system simulates a sensor producing percepts (timestamped event dictionaries) that an FSM-driven agent observes and reacts to. The repository includes a `sensor_agent.py` that periodically appends percepts to `event_logs.txt` and a new FSM watcher `lab3_agent.py` that reads those logs and executes reactive behaviors.

**Goals**
- **Rescue goal:** Safely locate affected sites and reduce damage to acceptable levels (e.g., damage <= 20) by allocating rescue resources and performing on-scene actions.
- **Response goal:** Quickly evaluate incoming events and allocate appropriate response resources (rapid or standard) based on severity and damage.

**Event triggering**
- Events are recorded as Python dict representations in `event_logs.txt` with keys `timestamp`, `severity`, and `damage`.
- The FSM agent (`lab3_agent.py`) tails `event_logs.txt`, parses each new line with `ast.literal_eval`, and treats each parsed dict as an input event that may trigger state transitions.

**FSM (diagram)**
- See the diagram: [fsm_diagram.mmd](fsm_diagram.mmd#L1)
- States: IDLE → ALERT → RESPONDING → RESCUING → RECOVERING → IDLE
- Representative transitions:
  - IDLE -> ALERT on new_event (severity != "none")
  - ALERT -> RESPONDING when response allocated
  - RESPONDING -> RESCUING on arrival (high severity or large damage)
  - RESCUING -> RECOVERING on rescue completion
  - RECOVERING -> IDLE when mission closed

**Implementation details**
- File: [lab3_agent.py](lab3_agent.py#L1)
  - `FSMAgent` encapsulates the state and transition logic.
  - `follow_file()` implements a tail-like generator to read appended lines from `event_logs.txt`.
  - `handle_event()` applies transition logic based on `severity` and `damage`.
  - Transitions and actions are logged to `lab3_execution.txt` for traceability.
- The existing `sensor_agent.py` produces percepts used to trigger the FSM; percept strings are parsed with `ast.literal_eval`.

**Execution trace**
- Full sample trace: [lab3_execution.txt](lab3_execution.txt#L1)
- Example summary from the trace:
  - Observed a medium-severity event (damage 30) → transitioned IDLE -> ALERT -> RESPONDING (standard response allocated).
  - Observed a high-severity event (damage 80) → transitioned RESPONDING -> RESCUING, performed rescue actions reducing damage, then RECOVERING -> IDLE.

**How to run (quick)**
1. Start the FSM watcher (reads `event_logs.txt` and writes `lab3_execution.txt`):
```bash
python lab3_agent.py
```
2. Produce events:
  - Run the sensor (requires SPADE environment):
```bash
python sensor_agent.py --period 2
```
  - Or inject an event manually:
```bash
echo "{'timestamp':'$(date -u +%Y-%m-%dT%H:%M:%SZ)','severity':'high','damage':80}" >> event_logs.txt
```
3. Watch transitions in `lab3_execution.txt` or on stdout.

**Observations & conclusions**
- The FSM provides a concise structure tying goals to reactive behaviors: the `ALERT`/`RESPONDING` stages map to the response goal, while `RESCUING`/`RECOVERING` map to the rescue goal.
- Simple numeric checks on `severity` and `damage` are sufficient for demonstration; in a full system, richer percept interpretation and resource models would be needed.

**Files added/modified**
- [lab3_agent.py](lab3_agent.py#L1) — FSM implementation and file-following logic.
- [fsm_diagram.mmd](fsm_diagram.mmd#L1) — Mermaid FSM diagram.
- [lab3_execution.txt](lab3_execution.txt#L1) — sample execution trace.

---
Prepared on: %s
