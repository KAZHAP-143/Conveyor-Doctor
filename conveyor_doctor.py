import math
import csv
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).with_name("conveyor_checks.csv")

# Practice limits — not validated equipment limits.
MAX_CURRENT = 3.0  # amperes
MIN_SPEED = 0.4    # metres per second

print("CONVEYOR DOCTOR")
print("Mode: Simulation — manually entered readings")

check_number = 0

while True:
    print("\nEnter readings, or type q to quit.")

    current_text = input("Motor current (A): ").strip()
    if current_text.lower() == "q":
        break

    speed_text = input("Belt speed (m/s): ").strip()
    if speed_text.lower() == "q":
        break

    try:
        motor_current = float(current_text)
        belt_speed = float(speed_text)
    except ValueError:
        print("Please enter numbers only.")
        continue

    if not math.isfinite(motor_current) or not math.isfinite(belt_speed):
        print("Please enter finite numbers.")
        continue

    if motor_current < 0 or belt_speed < 0:
        print("Readings cannot be negative.")
        continue

    check_number += 1

    high_current = motor_current > MAX_CURRENT
    low_speed = belt_speed < MIN_SPEED

    current_margin = MAX_CURRENT - motor_current
    speed_margin = belt_speed - MIN_SPEED
    result = (
        "CHECK REQUIRED"
        if high_current or low_speed
        else "HEALTH CHECK PASSED"
    )

    needs_header = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if needs_header:
            writer.writerow([
                "timestamp",
                "mode",
                "motor_current_A",
                "belt_speed_m_s",
                "high_current",
                "low_speed",
                "result",
            ])

        writer.writerow([
            datetime.now().astimezone().isoformat(timespec="seconds"),
            "simulation",
            motor_current,
            belt_speed,
            high_current,
            low_speed,
            result,
        ])

    print(f"Check saved to: {LOG_FILE.name}")
    print(f"\n--- Check {check_number} ---")
    print(f"Motor current: {motor_current:.2f} A")
    print(f"Belt speed: {belt_speed:.2f} m/s")
    print(f"Maximum allowed current: {MAX_CURRENT:.2f} A")
    print(f"Minimum allowed speed: {MIN_SPEED:.2f} m/s")
    print(f"Current margin: {current_margin:.2f} A")
    print(f"Speed margin: {speed_margin:.2f} m/s")

    if high_current:
        print("WARNING: High motor current — investigate load or resistance.")

    if low_speed:
        print("WARNING: Low belt speed — investigate the drive or belt.")

    if high_current or low_speed:
        print("RESULT: CHECK REQUIRED")
    else:
        print("RESULT: HEALTH CHECK PASSED")

print(f"\nSession ended. Completed checks: {check_number}")