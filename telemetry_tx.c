#ifdef __has_include
#  if __has_include(<stdint.h>)
#    include <stdint.h>
#  else
typedef unsigned int uint32_t;
#  endif
#else
#  include <stdint.h>
#endif
#include <stdio.h>
#include <time.h>

#include "telemetry_frame.h"

/* ---------------- Configuration ---------------- */

#define LOOP_PERIOD_MS   50

/* ---------------- Time utility ---------------- */

static uint32_t millis(void)
{
    return (uint32_t)(clock() * 1000 / CLOCKS_PER_SEC);
}

/* ---------------- Sensor simulation ---------------- */

static void read_sensors(float *ax, float *ay, float *az,
                         float *gx, float *gy, float *gz,
                         float *alt, float *temp)
{
    static float t = 0.0f;
    t += 0.05f;

    *ax = 0.02f * t;
    *ay = 0.98f;
    *az = 1.01f;

    *gx = 1.5f;
    *gy = 0.3f;
    *gz = 0.1f;

    *alt  = 120.4f;
    *temp = 26.1f;
}

/* ---------------- UART stub ---------------- */

static void uart_send(const char *data)
{
    /* In real firmware: send over UART */
    /* Here: placeholder */
    printf("%s", data);
}

/* ---------------- Main firmware loop ---------------- */

int main(void)
{
    char frame[160];

    uint32_t start_time = millis();

    while (1)
    {
        uint32_t loop_start = millis();

        float ax, ay, az;
        float gx, gy, gz;
        float alt, temp;

        /* Step 1: Read sensors */
        read_sensors(&ax, &ay, &az,
                     &gx, &gy, &gz,
                     &alt, &temp);

        /* Step 2: Build telemetry frame */
        build_l1_frame(frame,
                       loop_start - start_time,
                       ax, ay, az,
                       gx, gy, gz,
                       alt, temp);

        /* Step 3: Transmit frame */
        uart_send(frame);

        /* Step 4: Maintain 20 Hz loop */
        while ((millis() - loop_start) < LOOP_PERIOD_MS)
        {
            /* wait */
        }
    }
}
