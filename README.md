# Conveyor Doctor

A beginner engineering project developing a conveyor health-check
simulation toward future PLC implementation.

## Current features

- Manual entry of simulated motor current and belt speed
- Rejection of text, negative values, and non-finite numbers
- Separate high-current and low-speed warnings
- Repeated checks in one session
- Timestamped CSV logging
- History viewer with warning counts
- Graphing script for saved readings

## Practice limits

- High current: above 3.0 A
- Low speed: below 0.4 m/s
- Values exactly at these limits pass their respective checks.

These are learning thresholds, not validated equipment limits.

## Run

Enter readings and save checks:

python conveyor_doctor.py

View saved history:

python view_history.py

Plot saved history:

python plot_history.py

The graph requires matplotlib.

## Test results

The four manually tested conditions produced the expected results:

| Current (A) | Speed (m/s) | Expected result |
|---|---|---|
| 2.0 | 0.5 | Passed |
| 4.0 | 0.5 | High-current warning |
| 2.0 | 0.2 | Low-speed warning |
| 4.0 | 0.2 | Both warnings |

CSV logging and history counts were checked with these four cases.
Graph execution still needs confirmation.

## Limitations

All readings are manually entered simulation values.
The program checks thresholds; it cannot establish a mechanical
fault's cause. It does not yet control a motor or implement a PLC
pre-start sequence.

## Next development

- Verify graph output
- Introduce a simulated start and diagnostic sequence
- Compare readings with a healthy baseline
- Handle missing sensor data
- Develop PLC inputs, outputs, and sequence logic## Pre-start sequence simulation

Run with:

python prestart_sequence.py

Commands:
- check: perform a simulated diagnostic test
- run: allowed only after a healthy check
- stop: turn simulated operation off and clear start permission
- reset: clear a fault; a fresh check is still required
- q: exit with simulated motor off

A fault remains active after stop.
Reset does not automatically restart the conveyor.

This terminal simulation does not continuously monitor a running
conveyor. Commands are accepted only at the command prompt.## Missing-data test

A blank motor-current entry with a speed of 0.5 m/s
produced FAULT and denied start permission.

The state log records state changes, but currently does not
record the readings, fault reasons, or rejected commands.
## Current demonstration workflow

Activate the project environment in PowerShell:

.\.venv\Scripts\Activate.ps1

Install dependencies:

python -m pip install -r requirements.txt

Create the synthetic baseline if it does not already exist:

python build_baseline.py

Run the integrated pre-start sequence:

python prestart_sequence.py

Enter:
1. check
2. healthy
3. run

The default runtime demonstration injects a combined fault
at sample 6. The simulated motor stops and the sequence enters FAULT.
A subsequent run command is denied.

Enter q to exit.

Generate a graph of the latest runtime:

python plot_runtime.py

Launch the saved-history dashboard:

python -m streamlit run dashboard.py

## Standalone runtime scenarios

Run:

python runtime_monitor.py

Choose healthy for ten healthy samples and normal completion.
Choose combined for a fault injected at sample 6.
Press Ctrl+C during monitoring to test user interruption.

The integrated sequence currently uses the default combined scenario.

## Evidence files

- healthy_baseline.json: synthetic baseline statistics and limits
- diagnostic_samples_v2.csv: diagnostic samples and applied limits
- runtime_samples_v2.csv: runtime samples, flags, and applied limits
- runtime_outcomes.csv: completed, faulted, or interrupted outcomes
- sequence_events_v2.csv: sequence events, selected reasons, and linked IDs

## Operating limitations

This is a software simulation with synthetic readings.
Baseline limits are educational and require physical validation.
The dashboard displays saved history rather than live equipment.
During runtime monitoring, typed commands are not processed;
Ctrl+C interrupts the demonstration.
The program is not an industrial safety controller.