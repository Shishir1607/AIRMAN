#ifndef TELEMETRY_FRAME_H
#define TELEMETRY_FRAME_H

#include <stdint.h>

void build_l1_frame(char *out_buf,
                    uint32_t timestamp_ms,
                    float ax, float ay, float az,
                    float gx, float gy, float gz,
                    float alt, float temp);

#endif
