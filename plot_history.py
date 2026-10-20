import csv
from pathlib import Path

import matplotlib.pyplot as plt

FOLDER = Path(__file__).resolve().parent
LOG_FILE = FOLDER / "conveyor_checks.csv"

if not LOG_FILE.exists():
    print("No history found. Save some checks first.")
else:
    with LOG_FILE.open(newline="", encoding="utf-8") as file:
        checks = list(csv.DictReader(file))

    if not checks:
        print("History contains no checks.")
    else:
        numbers = list(range(1, len(checks) + 1))
        currents = [float(row["motor_current_A"]) for row in checks]
        speeds = [float(row["belt_speed_m_s"]) for row in checks]

        fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

        axes[0].plot(numbers, currents, "o-", label="Simulated current")
        axes[0].axhline(
            3.0, color="red", linestyle="--", label="Practice maximum: 3 A"
        )
        axes[0].set_ylabel("Motor current (A)")
        axes[0].legend()
        axes[0].grid(alpha=0.3)

        axes[1].plot(
            numbers, speeds, "o-", color="green", label="Simulated speed"
        )
        axes[1].axhline(
            0.4, color="red", linestyle="--", label="Practice minimum: 0.4 m/s"
        )
        axes[1].set_ylabel("Belt speed (m/s)")
        axes[1].set_xlabel("Saved check number")
        axes[1].set_xticks(numbers)
        axes[1].legend()
        axes[1].grid(alpha=0.3)

        fig.suptitle("Conveyor Doctor — Simulated Check History")
        fig.tight_layout()

        output = FOLDER / "conveyor_history.png"
        fig.savefig(output, dpi=150)
        print(f"Graph saved to: {output}")

        plt.show()