import random

# Repeatable synthetic data for learning, not physical measurements.
rng = random.Random(42)

SCENARIOS = {
    "healthy": (2.0, 0.50),
    "high_current": (4.0, 0.50),
    "low_speed": (2.0, 0.20),
    "combined": (4.0, 0.20),
}


def generate_reading(scenario):
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")

    base_current, base_speed = SCENARIOS[scenario]

    current = base_current + rng.uniform(-0.10, 0.10)
    speed = base_speed + rng.uniform(-0.02, 0.02)

    return current, speed


if __name__ == "__main__":
    print("CONVEYOR DOCTOR — SYNTHETIC SENSOR DATA")

    for scenario in SCENARIOS:
        print(f"\nScenario: {scenario}")

        for sample in range(1, 6):
            current, speed = generate_reading(scenario)

            print(
                f"Sample {sample}: "
                f"current={current:.2f} A, "
                f"speed={speed:.3f} m/s"
            )