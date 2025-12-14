import time
import math
import random

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

        return ax, ay, az, gx, gy, gz, alt, temp
