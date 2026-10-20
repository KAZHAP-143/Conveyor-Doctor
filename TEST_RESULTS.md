# Conveyor Doctor — Test Results

All readings are synthetic. No physical motor or PLC is connected.

## Confirmed tests

| Test | Observed result |
|---|---|
| Healthy pre-start check | READY; run permitted |
| High current | FAULT; run denied |
| Low belt speed | FAULT; run denied |
| Combined fault | FAULT; run denied |
| Missing manual reading | FAULT; start permission denied |
| Stop while faulted | FAULT retained |
| Reset | Fresh diagnostic required |
| Injected runtime fault | Detected at sample 6; simulated motor OFF |
| Healthy runtime | 10 samples; COMPLETED, STOPPED |
| User interruption | 4 samples; INTERRUPTED, STOPPED |
| Fault runtime outcome | FAULT_DETECTED, FAULT |
| Runtime sample CSV | Readings and applied limits saved |
| Diagnostic sample CSV | Five populated rows; applied limits saved |
| Runtime graph | Generated; displayed in dashboard |
| Diagnostic graph | Generated successfully |
| Dashboard sample display | Six samples; one flagged; values matched |
| Dashboard first fault | Sample 6; both warnings |

## Verification pending

- [ ] Dashboard shows all three recorded runtime outcomes correctly.
- [ ] Updated CSV export includes the selected run's outcome.
- [ ] Interrupted-run export has four rows and INTERRUPTED,STOPPED.
- [x] Latest full-project syntax check passes.
- [ ] Final end-to-end demonstration passes.
- [ ] Backup archive is confirmed.

## Interpretation limits

Passing these tests demonstrates the exercised software behavior.
It does not establish physical diagnostic accuracy, stopping time,
industrial safety compliance, or suitability for real machinery.