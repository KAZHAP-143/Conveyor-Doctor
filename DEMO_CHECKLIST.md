# Conveyor Doctor — Final Demonstration Checklist

## 1. Start permission
- [ ] Run before a diagnostic is denied.
- [ ] A healthy diagnostic produces READY.
- [ ] Run after READY begins runtime monitoring.

## 2. Runtime fault
- [ ] The injected combined fault is detected at sample 6.
- [ ] The simulated motor turns OFF and the state becomes FAULT.
- [ ] Run while faulted is denied.
- [ ] Stop does not clear FAULT.
- [ ] Reset returns STOPPED and requires a fresh check.

## 3. Other runtime outcomes
- [x] Standalone healthy run completes with ten samples.
- [x] Standalone fault run records FAULT_DETECTED.
- [x] User interruption records INTERRUPTED and STOPPED.

## 4. Traceability
- [ ] Linked diagnostic ID resolves to five samples.
- [ ] Linked runtime ID resolves to six samples.
- [ ] The runtime outcome matches FAULT_DETECTED.

## 5. Dashboard
- [x] Saved samples, graph, limits, and first fault display.
- [ ] Completed outcome displays correctly.
- [ ] Fault outcome displays correctly.
- [ ] Interrupted outcome displays correctly.
- [ ] Selected-run download contains correct samples and outcome.

## 6. Delivery
- [ ] Final syntax check passes after all changes.
- [ ] README matches current behavior.
- [ ] Final project backup is created and confirmed.