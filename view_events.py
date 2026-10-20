import csv
from pathlib import Path

event_file = Path(__file__).with_name("sequence_events_v2.csv")

if not event_file.exists():
    print("No event log found. Run prestart_sequence.py first.")
else:
    with event_file.open(newline="", encoding="utf-8") as file:
        events = list(csv.DictReader(file))

    print("CONVEYOR DOCTOR — SIMULATED EVENT HISTORY")
    print(f"Total records: {len(events)}")

    for event in events[-15:]:
        print(
            f"{event['timestamp']} | "
            f"{event['state']} | "
            f"{event['reason']}"
        )
        known_fault_reasons = {
        "Missing or non-numeric diagnostic reading",
        "High current and low belt speed",
        "High motor current",
        "Low belt speed",
        "Unknown diagnostic scenario",
    }

        fault_events = []

    for event in events:
        if event["state"] != "FAULT":
            continue

        # Remove IDs before interpreting the reason.
        reason = event["reason"].split(" | ", 1)[0]

        if reason.startswith("Runtime FAULT_DETECTED:"):
            fault_events.append(event)
            continue

        # Remove a diagnostic scenario prefix, if present.
        diagnostic_reason = reason.split(": ", 1)[-1]

        if diagnostic_reason in known_fault_reasons:
            fault_events.append(event)

    denied_runs = [
        event for event in events
        if event["reason"]
        == "Run command denied: healthy check required"
    ]

    print("\nEVENT SUMMARY")
    print(f"Fault records with specific reasons: {len(fault_events)}")
    print(f"Denied run commands: {len(denied_runs)}")