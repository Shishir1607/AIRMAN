import time
import math
import random
import matplotlib.pyplot as plt
from collections import deque

# ---------------- Sensor Simulator ---------------- #

class SensorSimulator:
    def __init__(self):
        self.start_time = time.time()

    def read(self):
        t = time.time() - self.start_time

        ax = math.sin(t) + random.uniform(-0.02, 0.02)
        ay = math.cos(t) + random.uniform(-0.02, 0.02)
        az = 1.0 + random.uniform(-0.01, 0.01)

        gx = 10.0 * math.sin(0.5 * t)
        gy = 5.0  * math.cos(0.5 * t)
        gz = 2.0

        alt = 120.0 + 0.5 * math.sin(0.1 * t)
        temp = 25.0 + 1.0 * math.sin(0.05 * t)

        return t, ax, ay, az, gx, gy, gz, alt, temp


# ---------------- Plot Setup ---------------- #

window = 200  # number of samples to display
t_buf = deque(maxlen=window)

ax_buf = deque(maxlen=window)
ay_buf = deque(maxlen=window)
az_buf = deque(maxlen=window)

gx_buf = deque(maxlen=window)
gy_buf = deque(maxlen=window)
gz_buf = deque(maxlen=window)

alt_buf = deque(maxlen=window)
temp_buf = deque(maxlen=window)

sensor = SensorSimulator()

plt.ion()
fig, axs = plt.subplots(4, 1, figsize=(10, 8))

# ---------------- Main Loop ---------------- #

while True:
    t, ax, ay, az, gx, gy, gz, alt, temp = sensor.read()

    t_buf.append(t)
    ax_buf.append(ax)
    ay_buf.append(ay)
    az_buf.append(az)

    gx_buf.append(gx)
    gy_buf.append(gy)
    gz_buf.append(gz)

    alt_buf.append(alt)
    temp_buf.append(temp)

    # Clear plots
    for axp in axs:
        axp.cla()

    # Accelerometer
    axs[0].plot(t_buf, ax_buf, label="ax")
    axs[0].plot(t_buf, ay_buf, label="ay")
    axs[0].plot(t_buf, az_buf, label="az")
    axs[0].set_ylabel("Accel (g)")
    axs[0].legend()
    axs[0].grid(True)

    # Gyroscope
    axs[1].plot(t_buf, gx_buf, label="gx")
    axs[1].plot(t_buf, gy_buf, label="gy")
    axs[1].plot(t_buf, gz_buf, label="gz")
    axs[1].set_ylabel("Gyro (deg/s)")
    axs[1].legend()
    axs[1].grid(True)

    # Altitude
    axs[2].plot(t_buf, alt_buf)
    axs[2].set_ylabel("Altitude (m)")
    axs[2].grid(True)

    # Temperature
    axs[3].plot(t_buf, temp_buf)
    axs[3].set_ylabel("Temp (°C)")
    axs[3].set_xlabel("Time (s)")
    axs[3].grid(True)

    plt.pause(0.05)  # ~20 Hz update
