import csv
from datetime import datetime
from pathlib import Path
from uuid import uuid4
import time

from automatic_check import MAX_CURRENT, MIN_SPEED
from sensor_simulation import generate_reading


def monitor_demo(inject_fault=True):
    print("CONVEYOR DOCTOR — RUNTIME MONITOR DEMO")
    print("Synthetic data only. No physical motor connected.")
    print("Starts after an assumed healthy pre-start check.")
    print("Press Ctrl+C to end the demonstration.\n")

    state = "RUNNING"
    outcome = "IN_PROGRESS"
    run_id = uuid4().hex
    log_file = Path(__file__).with_name("runtime_samples_v2.csv")

    try:
        for sample in range(1, 11):
            # Introduce a synthetic fault from sample 6 onward.
            scenario = (
                "combined"
                if inject_fault and sample >= 6
                else "healthy"
            )
            current, speed = generate_reading(scenario)

            print(
                f"Sample {sample}: {current:.2f} A | "
                f"{speed:.3f} m/s"
            )

            high_current = current > MAX_CURRENT
            low_speed = speed < MIN_SPEED
            needs_header = (
                not log_file.exists()
                or log_file.stat().st_size == 0
            )

            with log_file.open("a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)

                if needs_header:
                    writer.writerow([
                        "run_id",
                        "timestamp",
                        "mode",
                        "scenario",
                        "sample_number",
                        "motor_current_A",
                        "belt_speed_m_s",
                        "high_current",
                        "low_speed",
                        "max_current_A",
                        "min_speed_m_s",
                    ])

                writer.writerow([
                    run_id,
                    datetime.now().astimezone().isoformat(
                        timespec="milliseconds"
                    ),
                    "simulation",
                    scenario,
                    sample,
                    current,
                    speed,
                    high_current,
                    low_speed,
                    MAX_CURRENT,
                    MIN_SPEED,
                ])

            if high_current or low_speed:
                state = "FAULT"
                outcome = "FAULT_DETECTED"
                print("Abnormal runtime reading detected.")
                print("Simulated motor OFF. Start permission cleared.")
                break

            time.sleep(1)

        else:
            state = "STOPPED"
            outcome = "COMPLETED"
            print("Demonstration completed. Simulated motor OFF.")

    except KeyboardInterrupt:
        state = "STOPPED"
        outcome = "INTERRUPTED"
        print("\nDemonstration interrupted. Simulated motor OFF.")

    outcome_file = Path(__file__).with_name("runtime_outcomes.csv")
    needs_header = (
        not outcome_file.exists()
        or outcome_file.stat().st_size == 0
    )

    with outcome_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if needs_header:
            writer.writerow([
                "run_id", "end_timestamp", "mode",
                "outcome", "final_state",
            ])

        writer.writerow([
            run_id,
            datetime.now().astimezone().isoformat(timespec="seconds"),
            "simulation",
            outcome,
            state,
        ])
    print(f"Final state: {state}")
    return state, run_id, outcome


if __name__ == "__main__":
    choice = input(
        "Runtime scenario: healthy or combined [combined]: "
    ).strip().lower()

    if choice not in {"", "healthy", "combined"}:
        print("Unknown scenario. Demonstration not started.")
    else:
        monitor_demo(inject_fault=choice != "healthy")