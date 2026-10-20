import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


FOLDER = Path(__file__).resolve().parent


def main():
    log_file = FOLDER / "runtime_samples_v2.csv"

    if not log_file.exists():
        print("No runtime data found. Run runtime_monitor.py first.")
        return

    with log_file.open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    if not rows:
        print("The runtime log is empty.")
        return

    run_id = rows[-1]["run_id"]
    batch = [row for row in rows if row["run_id"] == run_id]

    times = [datetime.fromisoformat(row["timestamp"]) for row in batch]
    seconds = [(value - times[0]).total_seconds() for value in times]
    currents = [float(row["motor_current_A"]) for row in batch]
    speeds = [float(row["belt_speed_m_s"]) for row in batch]

    fault_times = [
        seconds[index]
        for index, row in enumerate(batch)
        if row["high_current"] == "True" or row["low_speed"] == "True"
    ]

    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)

    axes[0].plot(seconds, currents, "o-", label="Synthetic current")
    axes[0].axhline(
        float(batch[0]["max_current_A"]), color="red", linestyle="--",
        label="Current baseline maximum"
    )
    axes[0].set_ylabel("Motor current (A)")

    axes[1].plot(seconds, speeds, "o-", color="green",
                 label="Synthetic speed")
    axes[1].axhline(
        float(batch[0]["min_speed_m_s"]), color="red", linestyle="--",
        label="Speed baseline minimum"
    )
    axes[1].set_ylabel("Belt speed (m/s)")
    axes[1].set_xlabel("Elapsed time from first logged sample (s)")

    for axis in axes:
        if fault_times:
            axis.axvline(
                fault_times[0], color="orange", linestyle=":",
                label="First logged fault"
            )
        axis.grid(alpha=0.3)
        axis.legend()

    fig.suptitle(f"Conveyor Doctor — Synthetic Runtime\nRun: {run_id[:8]}")
    fig.tight_layout()

    output = FOLDER / f"runtime_{run_id}.png"
    fig.savefig(output, dpi=150)
    print(f"Graph saved to: {output}")
    plt.show()


if __name__ == "__main__":
    main()