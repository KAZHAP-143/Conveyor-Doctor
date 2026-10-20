import json
from pathlib import Path
from statistics import mean, stdev

from sensor_simulation import generate_reading

readings = [generate_reading("healthy") for _ in range(100)]

currents = [current for current, speed in readings]
speeds = [speed for current, speed in readings]

current_mean = mean(currents)
speed_mean = mean(speeds)

current_std = stdev(currents)
speed_std = stdev(speeds)

# Learning rule: mean plus/minus three sample standard deviations.
max_current = current_mean + 3 * current_std
min_speed = max(0.0, speed_mean - 3 * speed_std)

baseline = {
    "mode": "synthetic",
    "sample_count": len(readings),
    "method": "mean +/- 3 sample standard deviations",
    "mean_current_A": current_mean,
    "std_current_A": current_std,
    "mean_speed_m_s": speed_mean,
    "std_speed_m_s": speed_std,
    "max_current_A": max_current,
    "min_speed_m_s": min_speed,
}

output = Path(__file__).with_name("healthy_baseline.json")
output.write_text(json.dumps(baseline, indent=2), encoding="utf-8")

print("CONVEYOR DOCTOR — SYNTHETIC HEALTHY BASELINE")
print(f"Samples: {len(readings)}")
print(f"Mean current: {current_mean:.3f} A")
print(f"Mean speed: {speed_mean:.3f} m/s")
print(f"Provisional maximum current: {max_current:.3f} A")
print(f"Provisional minimum speed: {min_speed:.3f} m/s")
print(f"Saved to: {output.name}")