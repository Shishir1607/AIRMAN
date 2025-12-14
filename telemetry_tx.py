print("Telemetry TX starting...")

import time
from sensors import SensorSimulator
from protocol import build_l1_frame

print("Imports OK")

LOOP_PERIOD = 0.05
sensor = SensorSimulator()
start_time = time.time()

print("Entering main loop")

with open("telemetry_stream.txt", "w") as f:
    try:
        while True:
            print("Loop iteration")

            loop_start = time.time()
            timestamp_ms = int((loop_start - start_time) * 1000)

            ax, ay, az, gx, gy, gz, alt, temp = sensor.read()

            frame = build_l1_frame(
                timestamp_ms,
                ax, ay, az,
                gx, gy, gz,
                alt, temp
            )

            f.write(frame)
            f.flush()

            time.sleep(LOOP_PERIOD)

    except KeyboardInterrupt:
        print("Telemetry stopped")
