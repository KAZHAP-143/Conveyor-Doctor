import csv
import io
from pathlib import Path

import streamlit as st

FOLDER = Path(__file__).resolve().parent
LOG_FILE = FOLDER / "runtime_samples_v2.csv"

st.set_page_config(page_title="Conveyor Doctor", layout="wide")

st.title("Conveyor Doctor")
st.caption("Software simulation — synthetic data, no physical motor connected.")

st.button("Refresh saved data")

if not LOG_FILE.exists():
    st.info("Run runtime_monitor.py first to generate data.")
    st.stop()

with LOG_FILE.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

if not rows:
    st.info("The runtime log has no samples.")
    st.stop()

run_ids = list(dict.fromkeys(row["run_id"] for row in rows))
run_id = st.selectbox(
    "Select a saved run",
    options=list(reversed(run_ids)),
)

batch = [row for row in rows if row["run_id"] == run_id]
latest = batch[-1]

fault_detected = any(
    row["high_current"] == "True" or row["low_speed"] == "True"
    for row in batch
)

outcome_file = FOLDER / "runtime_outcomes.csv"
selected_outcome = None

if outcome_file.exists():
    with outcome_file.open(newline="", encoding="utf-8") as file:
        outcomes = list(csv.DictReader(file))

    selected_outcome = next(
        (
            row for row in reversed(outcomes)
            if row["run_id"] == run_id
        ),
        None,
    )

if selected_outcome is not None:
    outcome = selected_outcome["outcome"]

    if outcome == "COMPLETED":
        st.success("Recorded outcome: healthy demonstration completed.")
    elif outcome == "FAULT_DETECTED":
        st.error("Recorded outcome: runtime fault detected.")
    elif outcome == "INTERRUPTED":
        st.warning("Recorded outcome: demonstration interrupted by user.")
    else:
        st.info(f"Recorded outcome: {outcome}")

    st.write(
        f"Recorded final state: {selected_outcome['final_state']} | "
        f"Ended: {selected_outcome['end_timestamp']}"
    )
elif fault_detected:
    st.error("Fault flagged in saved samples. No final outcome record available.")
else:
    st.info("No fault flagged in saved samples. Run completion is unknown.")

st.caption("Saved history only — this page does not show live motor status.")

left, middle, right = st.columns(3)

left.metric("Last current", f"{float(latest['motor_current_A']):.2f} A")
middle.metric("Last belt speed", f"{float(latest['belt_speed_m_s']):.3f} m/s")
right.metric("Saved samples", len(batch))

st.write(
    f"Recorded limits: maximum current "
    f"{float(latest['max_current_A']):.3f} A; minimum speed "
    f"{float(latest['min_speed_m_s']):.3f} m/s"
)

st.subheader("Saved samples")
display_rows = [
    {
        "Sample": int(row["sample_number"]),
        "Timestamp": row["timestamp"],
        "Scenario": row["scenario"],
        "Current (A)": round(float(row["motor_current_A"]), 3),
        "Speed (m/s)": round(float(row["belt_speed_m_s"]), 3),
        "High current": row["high_current"] == "True",
        "Low speed": row["low_speed"] == "True",
    }
    for row in batch
]

st.dataframe(display_rows, use_container_width=True, hide_index=True)

graph_file = FOLDER / f"runtime_{run_id}.png"

if graph_file.exists():
    st.subheader("Runtime graph")
    st.image(str(graph_file))
else:
    st.info("No saved graph for this run. Run plot_runtime.py to graph the latest run.")

st.subheader("Export selected run")

export_rows = [
    {
        **row,
        "run_outcome": (
            selected_outcome["outcome"]
            if selected_outcome is not None
            else "UNKNOWN"
        ),
        "final_state": (
            selected_outcome["final_state"]
            if selected_outcome is not None
            else "UNKNOWN"
        ),
    }
    for row in batch
]

csv_buffer = io.StringIO()
writer = csv.DictWriter(
    csv_buffer,
    fieldnames=list(export_rows[0].keys()),
)
writer.writeheader()
writer.writerows(export_rows)

st.download_button(
    label="Download this run as CSV",
    data=csv_buffer.getvalue(),
    file_name=f"runtime_{run_id}.csv",
    mime="text/csv",
)
st.subheader("Selected run summary")

peak_current = max(float(row["motor_current_A"]) for row in batch)
minimum_speed = min(float(row["belt_speed_m_s"]) for row in batch)

flagged_samples = sum(
    row["high_current"] == "True" or row["low_speed"] == "True"
    for row in batch
)

first, second, third = st.columns(3)

first.metric("Peak current", f"{peak_current:.3f} A")
second.metric("Lowest belt speed", f"{minimum_speed:.3f} m/s")
third.metric("Flagged samples", flagged_samples)

st.caption(
    "A sample with both warnings counts as one flagged sample. "
    "Values describe saved synthetic data, not live equipment."
)
st.subheader("First recorded fault")

first_fault = next(
    (
        row for row in batch
        if row["high_current"] == "True"
        or row["low_speed"] == "True"
    ),
    None,
)

if first_fault is None:
    st.info("No fault is flagged in this run's saved samples.")
else:
    warnings = []

    if first_fault["high_current"] == "True":
        warnings.append("high motor current")

    if first_fault["low_speed"] == "True":
        warnings.append("low belt speed")

    st.warning(
        f"Sample {first_fault['sample_number']}: "
        + " and ".join(warnings)
    )
    st.write(f"Recorded at: {first_fault['timestamp']}")