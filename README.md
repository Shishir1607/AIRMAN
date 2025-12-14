# AIRMAN — Firmware Developer Technical Assignment  
**Level 1 Submission**

---

## 1. Overview

This project implements a **basic telemetry pipeline** that mimics an embedded firmware system transmitting sensor data at a fixed rate and a host-side receiver that validates, parses, and logs the data.

The solution is designed with a **firmware-first mindset**, emphasizing deterministic timing, clean protocol design, and reliability.

The implementation consists of:
- A **C-based telemetry transmitter** that simulates sensor readings, constructs telemetry frames, and runs in a fixed-rate main loop.
- A **Python-based receiver** that validates telemetry frames, parses sensor values, and logs valid data into a CSV file.

---

## 2. Project Structure

AIRMAN/
│
├── telemetry_tx.c # Firmware-style telemetry transmitter (C)
├── telemetry_frame.c # Telemetry frame builder + XOR checksum (C)
├── telemetry_frame.h # Frame builder interface (C)
│
├── sensors.py # Sensor simulation (Python)
├── protocol.py # Reference telemetry framing logic (Python)
├── uart_rx.py # Telemetry receiver + CSV logger (Python)
├── test_protocol.py # Telemetry frame test (Python)
│
└── README.md


---

## 3. Level 1 Implementation Details

### 3.1 Sensor Data Generation

Sensor data is **simulated** to emulate realistic embedded sensors while keeping the model simple and deterministic.

The following values are generated:
- Accelerometer: `ax, ay, az`
- Gyroscope: `gx, gy, gz`
- Altitude
- Temperature

In the C transmitter, sensor values are generated inside a dedicated `read_sensors()` function, mimicking how real firmware reads data from IMU and environmental sensors.

This approach ensures predictable behavior suitable for telemetry testing and validation.

---

### 3.2 Telemetry Frame Format

Telemetry frames strictly follow the Level-1 specification:
$L1,<timestamp_ms>,<ax>,<ay>,<az>,<gx>,<gy>,<gz>,<alt>,<temp>*<CHK>


Where:
- `$` indicates the start of a frame
- `L1` denotes Level-1 telemetry
- Fields are comma-separated
- `*` separates payload and checksum
- `CHK` is an XOR checksum in hexadecimal format

Example frame:
$L1,1234,0.020,0.980,1.010,1.50,0.30,0.10,120.40,26.10*52


---

### 3.3 XOR Checksum

The checksum is computed as follows:
- XOR of the ASCII values of **all characters between `$` and `*`**
- `$` and `*` are excluded
- The result is encoded as a two-digit hexadecimal value

This logic is implemented in:
- `telemetry_frame.c` (C firmware reference)
- `protocol.py` (Python reference implementation)

Any change in the payload results in a corresponding change in the checksum, ensuring data integrity.

---

### 3.4 Firmware Transmitter (C)

The telemetry transmitter is implemented entirely in **C**, following a firmware-style architecture:

- Infinite `while(1)` main loop
- Fixed 20 Hz execution rate (50 ms period)
- Millisecond timestamp generation
- Sensor read → frame build → UART transmit sequence

UART transmission is abstracted using a stub function (`uart_send()`), which currently outputs to standard output. This abstraction represents a real UART driver on embedded hardware.

The transmitter code is written to be **portable and microcontroller-friendly**, with:
- No dynamic memory allocation
- Fixed-size buffers
- Clear separation between sensor logic, protocol logic, and transmission

---

### 3.5 Receiver & CSV Logger (Python)

The Python receiver performs the following tasks:
1. Reads incoming telemetry frames
2. Validates frame structure and XOR checksum
3. Parses CSV fields
4. Logs valid telemetry data to `output.csv`
5. Prints formatted sensor values to the terminal

Malformed frames or checksum failures are safely ignored, demonstrating defensive programming practices typical of ground-station software.

---

## 4. How to Run (Host Side)

> Note: The C transmitter is provided as firmware reference code and is not required to be compiled locally.

### 4.1 Test Telemetry Frame Logic and to run UART Receiver

```bash
py test_protocol.py
py uart_rx.py
```

## 5. Assumptions & Simplifications

- Sensor data is simulated (no physical hardware used)
- UART transmission is abstracted as console output
- Timing accuracy is demonstrated conceptually
- Floating-point formatting is fixed for deterministic checksums
- No visualization is included, as per Level-1 requirements

## 6. AI Tool Usage
- AI tools were used to:
- Validate checksum logic
- Review protocol formatting
- Improve code clarity and documentation structure