# Lab 3 — Goals, Events, and Reactive Behavior (Fire Disaster)

**Objective**
- Model agent goals and event-triggered reactive behavior using a Finite State Machine (FSM) for a fire disaster response scenario.

**Background**
- The system simulates a fire sensor producing percepts (timestamped fire event dictionaries) that an FSM-driven agent observes and reacts to. The `sensor_agent.py` periodically appends fire percepts to `event_logs.txt`, and the FSM watcher `lab3_agent.py` reads those logs and executes reactive fire response behaviors.

**Goals**
- **Suppression Goal:** Actively suppress the fire on scene and reduce damage to acceptable levels (damage <= 20) by deploying appropriate fire units based on fire type.
- **Response Goal:** Quickly evaluate incoming fire events and dispatch the appropriate response (rapid or standard fire units) based on severity, spread rate, and damage.

**Event triggering**
- Fire events are recorded as Python dict representations in `event_logs.txt` with keys `timestamp`, `severity`, `damage`, `fire_type`, `location`, `spread_rate`, and `casualties`.
- The FSM agent (`lab3_agent.py`) tails `event_logs.txt`, parses each new line with `ast.literal_eval`, and treats each parsed dict as a fire input event that may trigger state transitions.

**FSM (diagram)**
- See the diagram: [fsm_diagram.mmd](fsm_diagram.mmd)
- States: IDLE → ALERT → RESPONDING → SUPPRESSING → RECOVERING → IDLE
- Representative transitions:
  - `IDLE -> ALERT` on `fire_detected` (severity != "none")
  - `ALERT -> RESPONDING` when fire units are dispatched
  - `RESPONDING -> SUPPRESSING` on units arriving on scene
  - `SUPPRESSING -> RECOVERING` when fire is contained
  - `RECOVERING -> IDLE` when site is cleared and mission is closed

**Response level logic**
| Condition | Response |
|---|---|
| `spread_rate >= 5.0 m/min` OR `damage >= 70` | `dispatch_rapid_fire_units` |
| Otherwise | `dispatch_standard_fire_units` |

**Implementation details**
- File: [lab3_agent.py](lab3_agent.py)
  - `FireResponseAgent` encapsulates the state and transition logic.
  - `handle_event()` reads `fire_type`, `spread_rate`, `location`, and `casualties` from each percept and applies transition logic.
  - `random_suppression()` simulates a 20–60 point damage reduction during the SUPPRESSING state.
  - Transitions and actions are logged to `lab3_execution.txt` for traceability.
- The existing `sensor_agent.py` produces fire percepts used to trigger the FSM; percept strings are parsed with `ast.literal_eval`.

**Execution trace (sample)**
```
LAB3_AGENT_STARTED
EVENT: {'severity': 'high', 'damage': 50, 'fire_type': 'structural', 'location': 'Block B', 'spread_rate': 5.7, 'casualties': 3}
STATE: IDLE -> ALERT (fire_detected | type=structural, location=Block B, spread_rate=5.7m/min)
STATE: ALERT -> RESPONDING (dispatch_rapid_fire_units | casualties=3)
STATE: RESPONDING -> SUPPRESSING (units_arrived_on_scene | fire_type=structural)
STATE: SUPPRESSING -> RECOVERING (fire_contained | damage reduced to 12)
STATE: RECOVERING -> IDLE (site_cleared | mission_closed)
```

**How to run (quick)**
1. Start the FSM watcher:
```bash
python3 lab3_agent.py
```
2. Produce fire events via the sensor agent:
```bash
python3 sensor_agent.py --period 2
```
3. Or inject a fire event manually:
```bash
echo "{'timestamp':'$(date -u +%Y-%m-%dT%H:%M:%SZ)','severity':'critical','damage':85,'fire_type':'wildfire','location':'Forest Zone','spread_rate':9.2,'casualties':7}" >> ../lab2/event_logs.txt
```
4. Watch transitions in `lab3_execution.txt` or on stdout.

**Observations & conclusions**
- The FSM provides a clear structure tying goals to reactive fire response behaviors: the `ALERT`/`RESPONDING` stages map to the Response Goal, while `SUPPRESSING`/`RECOVERING` map to the Suppression Goal.
- Using `spread_rate` and `casualties` alongside `severity` and `damage` gives a more realistic and nuanced fire dispatch decision than severity alone.
- In a full system, richer resource models (truck availability, water supply) and real-time sensor feeds would replace the simulated percepts.

**Files added/modified**
- [lab3_agent.py](lab3_agent.py) — Fire FSM implementation.
- [fsm_diagram.mmd](fsm_diagram.mmd) — Updated Mermaid FSM diagram.
- [lab3_execution.txt](lab3_execution.txt) — Sample execution trace.

---
Prepared on: 2026-02-26