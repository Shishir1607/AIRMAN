import matplotlib.pyplot as plt
import time

# ---------------- Data buffers ----------------
time_sec = []

ax_l, ay_l, az_l = [], [], []
gx_l, gy_l, gz_l = [], [], []
alt_l = []
temp_l = []

start_ts = None

# ---------------- Plot setup ----------------
plt.ion()
fig, axs = plt.subplots(4, 1, figsize=(10, 8), sharex=True)

# Accelerometer
line_ax, = axs[0].plot([], [], label="ax")
line_ay, = axs[0].plot([], [], label="ay")
line_az, = axs[0].plot([], [], label="az")
axs[0].set_ylabel("Accel (g)")
axs[0].set_title("Accelerometer")
axs[0].legend()
axs[0].grid(True)

# Gyroscope
line_gx, = axs[1].plot([], [], label="gx")
line_gy, = axs[1].plot([], [], label="gy")
line_gz, = axs[1].plot([], [], label="gz")
axs[1].set_ylabel("Gyro (deg/s)")
axs[1].set_title("Gyroscope")
axs[1].legend()
axs[1].grid(True)

# Altitude
line_alt, = axs[2].plot([], [], label="alt")
axs[2].set_ylabel("Altitude (m)")
axs[2].set_title("Altitude")
axs[2].legend()
axs[2].grid(True)

# Temperature
line_temp, = axs[3].plot([], [], label="temp")
axs[3].set_ylabel("Temp (°C)")
axs[3].set_xlabel("Time (s)")
axs[3].set_title("Temperature")
axs[3].legend()
axs[3].grid(True)

# ---------------- Open telemetry file ----------------
with open("telemetry_stream.txt", "r") as f:
    f.seek(0, 2)  # jump to end of file
    print("Live telemetry plot running...")

    while True:
        line = f.readline()

        if not line:
            time.sleep(0.05)
            continue

        if not line.startswith("$L1"):
            continue

        try:
            payload, chk = line[1:].split("*")
            fields = payload.split(",")

            ts = int(fields[1])
            ax, ay, az = float(fields[2]), float(fields[3]), float(fields[4])
            gx, gy, gz = float(fields[5]), float(fields[6]), float(fields[7])
            alt = float(fields[8])
            temp = float(fields[9])

            if start_ts is None:
                start_ts = ts

            t = (ts - start_ts) / 1000.0
            time_sec.append(t)

            ax_l.append(ax); ay_l.append(ay); az_l.append(az)
            gx_l.append(gx); gy_l.append(gy); gz_l.append(gz)
            alt_l.append(alt)
            temp_l.append(temp)

            # ---- Update plots ----
            line_ax.set_data(time_sec, ax_l)
            line_ay.set_data(time_sec, ay_l)
            line_az.set_data(time_sec, az_l)

            line_gx.set_data(time_sec, gx_l)
            line_gy.set_data(time_sec, gy_l)
            line_gz.set_data(time_sec, gz_l)

            line_alt.set_data(time_sec, alt_l)
            line_temp.set_data(time_sec, temp_l)

            for axp in axs:
                axp.relim()
                axp.autoscale_view()

            plt.pause(0.01)

        except Exception:
            pass
