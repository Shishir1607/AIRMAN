import csv
import sys
from protocol import xor_checksum

# ---------------- Configuration ---------------- #

CSV_FILE = "output.csv"

# ---------------- Initialize CSV ---------------- #

csv_file = open(CSV_FILE, "w", newline="")
csv_writer = csv.writer(csv_file)

csv_writer.writerow([
    "timestamp_ms",
    "ax", "ay", "az",
    "gx", "gy", "gz",
    "alt", "temp"
])

print("Receiver started. Waiting for telemetry...\n")

# ---------------- Frame Processing ---------------- #

try:
    for line in sys.stdin:
        line = line.strip()

        # Basic frame validation
        if not line.startswith("$") or "*" not in line:
            continue

        payload, recv_chk = line[1:].split("*", 1)

        # Validate checksum
        calc_chk = xor_checksum(payload)

        try:
            recv_chk = int(recv_chk, 16)
        except ValueError:
            continue

        if calc_chk != recv_chk:
            print("Checksum error, frame dropped")
            continue

        # Parse CSV fields
        fields = payload.split(",")

        if fields[0] != "L1":
            continue

        # Extract data (skip 'L1')
        data = fields[1:]

        # Log to CSV
        csv_writer.writerow(data)
        csv_file.flush()

        # Pretty print
        print(
            f"TS={data[0]} ms | "
            f"AX={data[1]} AY={data[2]} AZ={data[3]} | "
            f"ALT={data[7]} m TEMP={data[8]} C"
        )

except KeyboardInterrupt:
    print("\nReceiver stopped.")

finally:
    csv_file.close()
