import csv
from pathlib import Path

import matplotlib.pyplot as plt


FOLDER = Path(__file__).resolve().parent
LOG_FILE = FOLDER / "diagnostic_samples_v2.csv"


def main():
    if not LOG_FILE.exists():
        print("No diagnostic samples found. Run automatic_check.py first.")
        return

    with LOG_FILE.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("The sample log is empty.")
        return

    latest_id = rows[-1]["check_id"]
    batch = [row for row in rows if row["check_id"] == latest_id]

    numbers = [int(row["sample_number"]) for row in batch]
    currents = [float(row["motor_current_A"]) for row in batch]
    speeds = [float(row["belt_speed_m_s"]) for row in batch]

    fig, axes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)

    axes[0].plot(numbers, currents, "o-", label="Synthetic current")
    axes[0].axhline(
        float(batch[0]["max_current_A"]), color="red", linestyle="--",
        label=f"Baseline maximum: {batch[0]['max_current_A']} A"
    )
    axes[0].set_ylabel("Motor current (A)")
    axes[0].legend()
    axes[0].grid(alpha=0.3)

    axes[1].plot(numbers, speeds, "o-", color="green",
                 label="Synthetic belt speed")
    axes[1].axhline(
        float(batch[0]["min_speed_m_s"]), color="red", linestyle="--",
        label=f"Baseline minimum: {batch[0]['min_speed_m_s']} m/s"
    )
    axes[1].set_ylabel("Belt speed (m/s)")
    axes[1].set_xlabel("Sample number — not elapsed time")
    axes[1].set_xticks(numbers)
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    fig.suptitle(
        f"Conveyor Doctor — {batch[0]['scenario']}\n"
        f"Synthetic diagnostic batch: {latest_id[:8]}"
    )
    fig.tight_layout()

    output = FOLDER / f"diagnostic_{latest_id}.png"
    fig.savefig(output, dpi=150)
    print(f"Graph saved to: {output}")
    plt.show()


if __name__ == "__main__":
    main()