from protocol import build_l1_frame

frame = build_l1_frame(
    timestamp_ms=1234,
    ax=0.02,
    ay=0.98,
    az=1.01,
    gx=1.5,
    gy=0.3,
    gz=0.1,
    alt=120.4,
    temp=26.1
)

print(frame)
