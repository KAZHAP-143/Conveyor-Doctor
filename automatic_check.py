import json
import csv
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from sensor_simulation import SCENARIOS, generate_reading
BASELINE_FILE = Path(__file__).with_name("healthy_baseline.json")

baseline = json.loads(BASELINE_FILE.read_text(encoding="utf-8"))

MAX_CURRENT = float(baseline["max_current_A"])
MIN_SPEED = float(baseline["min_speed_m_s"])


def run_diagnostic(scenario):
    print("\nLimits from synthetic healthy baseline:")
    print(f"Maximum current: {MAX_CURRENT:.3f} A")
    print(f"Minimum belt speed: {MIN_SPEED:.3f} m/s")
    readings = [generate_reading(scenario) for _ in range(5)]
    log_file = Path(__file__).with_name("diagnostic_samples_v2.csv")
    needs_header = not log_file.exists() or log_file.stat().st_size == 0

    check_id = uuid4().hex
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

    with log_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if needs_header:
            writer.writerow([
                "check_id",
                "timestamp",
                "mode",
                "scenario",
                "sample_number",
                "motor_current_A",
                "belt_speed_m_s",
                "max_current_A",
                "min_speed_m_s",
            ])

        for number, (current, speed) in enumerate(readings, start=1):
            writer.writerow([
                check_id,
                timestamp,
                "simulation",
                scenario,
                number,
                current,
                speed,
                MAX_CURRENT,
                MIN_SPEED,
            ])

    for number, (current, speed) in enumerate(readings, start=1):
        print(
            f"Sample {number}: "
            f"{current:.2f} A | {speed:.3f} m/s"
        )

    highest_current = max(current for current, speed in readings)
    lowest_speed = min(speed for current, speed in readings)

    high_current = highest_current > MAX_CURRENT
    low_speed = lowest_speed < MIN_SPEED

    if high_current and low_speed:
        reason = "High current and low belt speed"
    elif high_current:
        reason = "High motor current"
    elif low_speed:
        reason = "Low belt speed"
    else:
        reason = "Diagnostic readings within synthetic baseline limits"

    passed = not (high_current or low_speed)
    return passed, reason, check_id


if __name__ == "__main__":
    print("CONVEYOR DOCTOR — AUTOMATIC SIMULATED CHECK")
    print("Scenarios:", ", ".join(SCENARIOS))

    scenario = input("Choose a scenario: ").strip().lower()

    if scenario not in SCENARIOS:
        print("Unknown scenario. No diagnostic performed.")
    else:
        passed, reason, check_id = run_diagnostic(scenario)
        print(f"Check ID: {check_id}")

        print(f"\nReason: {reason}")
        print("RESULT:", "READY" if passed else "FAULT")