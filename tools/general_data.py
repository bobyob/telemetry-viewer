from pathlib import Path
import numpy as np
import pandas as pd

N = 600         # number of samples
DT_MS = 100     # one sample every 100ms (10Hz)


rng = np.random.default_rng(seed=0)     #random number generator for reproducibility
t_ms = np.arange(N) * DT_MS
t_s = t_ms / 1000

pack_current = 80 + 60 * np.sin(2 * np.pi * t_s / 20) + rng.normal(0, 5, N) # swings between 20A and 140A
pack_voltage = 400 - 0.3 * t_s - 0.05 * pack_current + rng.normal(0, 0.5, N) # starts ~400V, drains to ~375-385V, dips under high current
cell_temp_max = 25 + 0.25 * t_s + rng.normal(0, 0.2, N) # swings between 25°C and 30°C
motor_rpm = 50 * pack_current + rng.normal(0, 100, N) # swings between 1000 RPM and 7000 RPM

# Create a DataFrame and save to CSV
df = pd.DataFrame({                     # create a  using a dictionary
    "t_ms": t_ms,
    "pack_voltage": pack_voltage,
    "pack_current": pack_current,
    "cell_temp_max": cell_temp_max,
    "motor_rpm": motor_rpm,
})

Path("sample_data").mkdir(exist_ok=True)
df.round(2).to_csv("sample_data/fake_run.csv", index=False)
print(df.head())
print(f"Saved {len(df)} rows")


