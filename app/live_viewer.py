from collections import deque

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

# --- Settings ---
SENSORS = ["pack_voltage", "pack_current", "cell_temp_max", "motor_rpm"]
WINDOW_S = 10
DT_S = 0.1
MAX_POINTS = int(WINDOW_S / DT_S)

# --- Window ---
app = pg.mkQApp("Live Telemetry")
win = pg.GraphicsLayoutWidget(title="Live Telemetry")
win.resize(1000, 900)

# --- Storage ---
times = deque(maxlen=MAX_POINTS)
buffers = {}
curves = {}

first_plot = None
for row, name in enumerate(SENSORS):
    plot = win.addPlot(row=row, col=0, title=name)
    plot.setLabel("bottom", "Time", units="s")
    plot.showGrid(x=True, y=True)
    curves[name] = plot.plot(pen=pg.mkPen(width=2))
    buffers[name] = deque(maxlen=MAX_POINTS)
    if first_plot is None:
        first_plot = plot
    else:
        plot.setXLink(first_plot)

t = 0.0
bad_lines = 0


# --- Fake car: builds ONE TEXT LINE, exactly like the Teensy will send ---
# 🔌 TEENSY POINT: this function disappears; lines come from the serial port instead
def fake_car_line(t_now):
    current = 80 + 60 * np.sin(2 * np.pi * t_now / 20) + np.random.normal(0, 5)
    voltage = 400 - 0.3 * t_now - 0.05 * current + np.random.normal(0, 0.5)
    temp = 25 + 0.25 * t_now + np.random.normal(0, 0.2)
    rpm = 50 * current + np.random.normal(0, 100)
    t_ms = int(t_now * 1000)

    line = f"{t_ms},{voltage:.2f},{current:.2f},{temp:.2f},{rpm:.0f}\n"

    # Simulate a real-world glitch: ~2% of lines get cut off halfway
    if np.random.random() < 0.02:
        line = line[: len(line) // 2]

    return line


# --- Parser: turns one text line into numbers, or None if the line is bad ---
def parse_line(line):
    parts = line.strip().split(",")

    # Check 1: right number of values? (time + one per sensor)
    if len(parts) != 1 + len(SENSORS):
        return None

    # Check 2: can every piece become a number?
    numbers = []
    try:
        for p in parts:
            numbers.append(float(p))
    except ValueError:
        return None

    # Good line: split into time (in seconds) and a dictionary of sensor values
    t_s = numbers[0] / 1000
    reading = {}
    for i, name in enumerate(SENSORS):
        reading[name] = numbers[i + 1]   # +1 because position 0 is time

    return t_s, reading


# --- Called every 100 ms by the timer ---
def update():
    global t, bad_lines
    t = t + DT_S

    line = fake_car_line(t)        # 🔌 TEENSY POINT: becomes "read a line from serial"
    result = parse_line(line)

    if result is None:             # bad line: count it, skip it, keep going
        bad_lines = bad_lines + 1
        win.setWindowTitle(f"Live Telemetry   |   bad lines: {bad_lines}")
        return

    t_s, reading = result
    times.append(t_s)
    for name in SENSORS:
        buffers[name].append(reading[name])
        curves[name].setData(list(times), list(buffers[name]))


# --- Timer ---
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(int(DT_S * 1000))

win.show()
pg.exec()