/**
 * @file led_control.h
 * @brief LED control header file
 * @details Provides LED manipulation interfaces for embedded systems
 */

#ifndef LED_CONTROL_H
#define LED_CONTROL_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief LED identifiers
 */
typedef enum
{
    LED_NONE = 0,
    LED_STATUS,
    LED_ERROR,
    LED_ACTIVITY,
    LED_COUNT
} LedId_t;

/**
 * @brief LED states
 */
typedef enum
{
    LED_OFF = 0,
    LED_ON,
    LED_TOGGLE,
    LED_BLINK
} LedState_t;

/**
 * @brief Initialize LED control system
 * @return bool Success status
 */
bool LED_Init(void);

/**
 * @brief Set LED state
 * @param id LED identifier
 * @param state Desired state
 * @return bool Success status
 */
bool LED_Set(LedId_t id, LedState_t state);

/**
 * @brief Toggle LED state
 * @param id LED identifier
 * @return bool Success status
 */
bool LED_Toggle(LedId_t id);

/**
 * @brief Update all LEDs (called periodically)
 */
void LED_Update(void);

/**
 * @brief Set blink rate for LED
 * @param id LED identifier
 * @param rate_ms Blink rate in milliseconds
 * @return bool Success status
 */
bool LED_SetBlinkRate(LedId_t id, uint32_t rate_ms);

#ifdef __cplusplus
}
#endif

#endif /* LED_CONTROL_H */
