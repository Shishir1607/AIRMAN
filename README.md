# AIRMAN — Firmware Developer Technical Assignment  
**Level 1 Submission**

---

## 1. Overview

This project implements a **basic telemetry pipeline** that mirrors a real embedded firmware system transmitting sensor data at a fixed rate, along with host-side tools to validate, log, and visualize the data.

The solution follows a **firmware-first design philosophy**:
- Core telemetry framing and timing logic are written in **C** as portable firmware reference code.
- **Python** is used to simulate sensors, transmit telemetry, receive and validate frames, log data, and perform continuous visualization.

The emphasis is on **deterministic timing, clean protocol design, robustness, and clarity**, rather than platform-specific tooling.

---

## 2. Project Structure

AIRMAN/
│
├── telemetry_tx.c # Firmware-style telemetry transmitter (C reference)
├── telemetry_frame.c # Telemetry framing + XOR checksum (C)
├── telemetry_frame.h # Frame builder interface (C)
│
├── sensors.py # Sensor simulation module (Python)
├── protocol.py # Telemetry framing + checksum (Python)
├── telemetry_tx.py # Python transmitter (uses sensors.py)
├── uart_rx.py # Receiver, checksum validation & CSV logger
├── plot_live.py # Continuous live telemetry visualization
│
├── telemetry_stream.txt # Generated telemetry log
├── output.csv # Parsed telemetry data
│
└── README.md

---

## 3. Level 1 Implementation Details

### 3.1 Sensor Data Generation

Sensor data is **simulated** using a dedicated Python module (`sensors.py`) to emulate realistic embedded sensors:

- Accelerometer: `ax, ay, az`
- Gyroscope: `gx, gy, gz`
- Altitude
- Temperature

The simulator uses time-based sine and cosine functions with small noise components to generate smooth, predictable waveforms suitable for telemetry validation.

---

### 3.2 Telemetry Frame Format

Telemetry frames strictly follow the Level-1 specification:

$L1,<timestamp_ms>,<ax>,<ay>,<az>,<gx>,<gy>,<gz>,<alt>,<temp>*<CHK>


Where:
- `$` marks the start of the frame
- `L1` indicates Level-1 telemetry
- Fields are comma-separated
- `*` separates payload and checksum
- `CHK` is an XOR checksum encoded in hexadecimal

Example:
$L1,32254,0.756,0.680,0.993,-4.07,-4.57,2.00,119.96,26.00*6F


---

### 3.3 XOR Checksum

The checksum is calculated as:
- XOR of the ASCII values of all characters **between `$` and `*`**
- `$` and `*` are excluded
- The result is formatted as a two-digit hexadecimal value

This logic is implemented consistently in:
- `telemetry_frame.c` (firmware reference)
- `protocol.py` (Python implementation)

---

### 3.4 Firmware Transmitter (C Reference)

The C code (`telemetry_tx.c`) represents a **firmware-style telemetry transmitter**:

- Infinite `while(1)` main loop
- Fixed 20 Hz execution rate (50 ms period)
- Millisecond timestamping
- Sensor read → frame build → UART transmit sequence

UART transmission is abstracted using a stub function to keep the code portable across embedded targets.  
The C code is **not compiled locally** and is provided as a reference firmware implementation.

---

### 3.5 Python Transmitter

The Python transmitter (`telemetry_tx.py`) mirrors the firmware logic and is used for execution and demonstration:

- Reads sensor data from `sensors.py`
- Builds telemetry frames using `protocol.py`
- Runs at **20 Hz**
- Writes frames to `telemetry_stream.txt`

A file-based approach is used to ensure reliable telemetry flow on Windows systems and to allow offline replay and analysis.

---

### 3.6 Receiver & CSV Logger

The receiver (`uart_rx.py`) performs:

1. Reading telemetry frames from standard input
2. Validating frame structure and XOR checksum
3. Parsing sensor values
4. Logging valid data to `output.csv`
5. Printing formatted output to the terminal

Malformed frames or checksum failures are safely ignored.

---

### 3.7 Continuous Visualization

Live visualization is implemented in `plot_live.py`:

- Continuously reads new telemetry frames from `telemetry_stream.txt`
- Displays real-time plots for:
  - Accelerometer (`ax, ay, az`)
  - Gyroscope (`gx, gy, gz`)
  - Altitude
  - Temperature
- Uses interactive matplotlib updates for reliable real-time plotting on Windows

This provides immediate visual validation of sensor behavior and telemetry integrity.

---

## 4. How to Run

### 4.1 Generate Telemetry

```bash
py telemetry_tx.py
```

Let it run for a few seconds, then stop with Ctrl + C.
This generates telemetry_stream.txt.

### 4.2 Run Receiver & CSV Logger

```bash
Get-Content telemetry_stream.txt | py uart_rx.py
```

Parsed telemetry is printed to the terminal and logged into output.csv.


### 4.3 Run Continuous Visualization

With the transmitter running:

```bash
py plot_live.py
```

Graphs update continuously as new telemetry data is generated.

---

## 5. Assumptions & Simplifications

- Sensor data is simulated (no physical hardware used)

- UART transmission is abstracted

- Timing is conceptually deterministic (not hardware-clock precise)

- ASCII telemetry is used for clarity and debugging

- Visualization is implemented on the host side

These choices prioritize clarity, reliability, and debuggability.

---

## 6. AI Tool Usage

AI tools were used to:

- Review telemetry framing and checksum logic

- Assist with debugging strategies

- Improve documentation structure and clarity
