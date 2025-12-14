#include "telemetry_frame.h"
#include <stdio.h>

/*
 * Compute XOR checksum of ASCII characters in payload.
 * Payload must NOT include '$' or '*'.
 */
static uint8_t xor_checksum(const char *payload)
{
    uint8_t chk = 0;

    while (*payload)
    {
        chk ^= (uint8_t)(*payload);
        payload++;
    }

    return chk;
}

/*
 * Build Level-1 telemetry frame.
 *
 * Format:
 * $L1,<timestamp_ms>,<ax>,<ay>,<az>,<gx>,<gy>,<gz>,<alt>,<temp>*<CHK>
 */
void build_l1_frame(char *out_buf,
                    uint32_t timestamp_ms,
                    float ax, float ay, float az,
                    float gx, float gy, float gz,
                    float alt, float temp)
{
    char payload[128];

    /* Build payload (everything between $ and *) */
    snprintf(payload, sizeof(payload),
             "L1,%lu,%.3f,%.3f,%.3f,%.2f,%.2f,%.2f,%.2f,%.2f",
             (unsigned long)timestamp_ms,
             ax, ay, az,
             gx, gy, gz,
             alt, temp);

    uint8_t chk = xor_checksum(payload);

    /* Final frame */
    snprintf(out_buf, 160,
             "$%s*%02X\r\n",
             payload, chk);
}
