def xor_checksum(payload: str) -> int:
    """
    Compute XOR checksum of all characters in payload.
    Payload must NOT include '$' or '*'.
    """
    chk = 0
    for c in payload:
        chk ^= ord(c)
    return chk


def build_l1_frame(timestamp_ms,
                   ax, ay, az,
                   gx, gy, gz,
                   alt, temp):
    """
    Build a Level-1 telemetry frame.

    Format:
    $L1,<timestamp_ms>,<ax>,<ay>,<az>,<gx>,<gy>,<gz>,<alt>,<temp>*<CHK>
    """

    payload = (
        f"L1,{timestamp_ms},"
        f"{ax:.3f},{ay:.3f},{az:.3f},"
        f"{gx:.2f},{gy:.2f},{gz:.2f},"
        f"{alt:.2f},{temp:.2f}"
    )

    chk = xor_checksum(payload)

    frame = f"${payload}*{chk:02X}\n"
    return frame
