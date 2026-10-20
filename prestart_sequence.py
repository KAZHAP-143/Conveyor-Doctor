import math
import time
import csv
from datetime import datetime
from pathlib import Path
from automatic_check import run_diagnostic
from sensor_simulation import SCENARIOS
from runtime_monitor import monitor_demo

EVENT_FILE = Path(__file__).with_name("sequence_events_v2.csv")


def record_state(state, reason="State reached"):
    needs_header = (
        not EVENT_FILE.exists()
        or EVENT_FILE.stat().st_size == 0
    )

    with EVENT_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if needs_header:
            writer.writerow(["timestamp", "mode", "state", "reason"])

        writer.writerow([
            datetime.now().astimezone().isoformat(timespec="seconds"),
            "simulation",
            state,
            reason,
        ])
MAX_CURRENT = 3.0
MIN_SPEED = 0.4

state = "STOPPED"

print("CONVEYOR DOCTOR — VERSION 3")
print("Simulation only. No physical motor connected.")
print("Commands: check, run, stop, reset, q")

last_logged_state = None

while True:
    if state != last_logged_state:
        record_state(state)
        last_logged_state = state

    print(f"\nSTATE: {state}")
    command = input("Command: ").strip().lower()

    if command == "q":
        state = "STOPPED"
        record_state(state)
        print("Simulated motor OFF. Session ended.")
        break

    if command == "stop":
        if state != "FAULT":
            state = "STOPPED"
        print("Simulated motor OFF. Start permission cleared.")
        continue

    if command == "reset":
        if state == "FAULT":
            state = "STOPPED"
            print("Fault cleared. A new health check is required.")
        else:
            print("No fault to reset.")
        continue

    if command == "run":
        if state == "READY":
            state = "RUNNING"
            record_state(
                state,
                "Run command accepted after healthy diagnostic check"
            )
            last_logged_state = state

            state, run_id, outcome = monitor_demo()

            record_state(
                state,
                f"Runtime {outcome}: motor OFF | "
                f"check_id={check_id} | run_id={run_id}"
            )
            last_logged_state = state
        elif state == "RUNNING":
            print("Already running.")
        else:
            record_state(
                state,
                "Run command denied: healthy check required"
            )
            print("Run denied. Complete a healthy check first.")
        continue

    if command == "check":
        if state != "STOPPED":
            print("Stop first, or reset if a fault is active.")
            continue

        state = "PRE-START WARNING"
        record_state(state)
        print(f"STATE: {state}")
        time.sleep(2)

        state = "DIAGNOSTIC RUN"
        record_state(state)
        print(f"STATE: {state}")
        print("Simulated motor test.")
        time.sleep(2)

        state = "EVALUATING"
        record_state(state)
        print("Simulated motor OFF.")
        print(f"STATE: {state}")

        print("Scenarios:", ", ".join(SCENARIOS))
        scenario = input(
            "Choose simulated scenario, or cancel: "
        ).strip().lower()

        if scenario == "cancel":
            state = "STOPPED"
            record_state(state, "Diagnostic cancelled")
            last_logged_state = state
            print("Check cancelled. Start permission cleared.")
            continue

        if scenario not in SCENARIOS:
            state = "FAULT"
            record_state(state, "Unknown diagnostic scenario")
            last_logged_state = state
            print("Unknown scenario. Start permission denied.")
            continue

        passed, reason, check_id = run_diagnostic(scenario)

        state = "READY" if passed else "FAULT"
        record_state(
            state,
            f"{scenario}: {reason} | check_id={check_id}"
        )
        last_logged_state = state

        print(f"Reason: {reason}")

        if passed:
            print("Health check passed. Motor remains OFF.")
            print("Type run to start simulated operation.")
        else:
            print("Start permission denied.")

        continue