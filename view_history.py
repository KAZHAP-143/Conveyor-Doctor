import csv
from pathlib import Path

log_file = Path(__file__).with_name("conveyor_checks.csv")

if not log_file.exists():
    print("No history file found. Run conveyor_doctor.py and save a check first.")
else:
    with log_file.open(newline="", encoding="utf-8") as file:
        checks = list(csv.DictReader(file))

    print("CONVEYOR DOCTOR — SIMULATED CHECK HISTORY")
    print(f"Total saved checks: {len(checks)}")

    for check in checks[-5:]:
        print(
            f"{check['timestamp']} | "
            f"{check['motor_current_A']} A | "
            f"{check['belt_speed_m_s']} m/s | "
            f"{check['result']}"
        )
        passed = sum(
        check["result"] == "HEALTH CHECK PASSED"
        for check in checks
    )
    flagged = len(checks) - passed

    high_current_count = sum(
        check["high_current"] == "True"
        for check in checks
    )
    low_speed_count = sum(
        check["low_speed"] == "True"
        for check in checks
    )

    print("\nSUMMARY")
    print(f"Passed checks: {passed}")
    print(f"Checks requiring attention: {flagged}")
    print(f"High-current warnings: {high_current_count}")
    print(f"Low-speed warnings: {low_speed_count}")