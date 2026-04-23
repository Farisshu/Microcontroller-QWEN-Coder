/**
 * @file led_control.c
 * @brief LED control implementation
 * @details Provides LED manipulation functionality for embedded systems
 */

#include "led_control.h"
#include "hal.h"
#include <string.h>

/**
 * @brief LED configuration structure
 */
typedef struct
{
    LedId_t id;
    uint8_t pin;
    LedState_t state;
    bool is_on;
    uint32_t blink_rate_ms;
    uint32_t last_toggle_time;
} LedConfig_t;

/**
 * @brief LED registry
 */
static LedConfig_t xLeds[LED_COUNT];

/**
 * @brief System tick counter (simulated)
 */
static uint32_t u32SystemTick = 0U;

/**
 * @brief Initialize LED control system
 */
bool LED_Init(void)
{
    uint8_t u8Index;
    bool bResult = true;
    
    memset(xLeds, 0, sizeof(xLeds));
    
    /* Configure LED pins */
    xLeds[LED_STATUS].id = LED_STATUS;
    xLeds[LED_STATUS].pin = 0U;
    xLeds[LED_STATUS].state = LED_OFF;
    
    xLeds[LED_ERROR].id = LED_ERROR;
    xLeds[LED_ERROR].pin = 1U;
    xLeds[LED_ERROR].state = LED_OFF;
    
    xLeds[LED_ACTIVITY].id = LED_ACTIVITY;
    xLeds[LED_ACTIVITY].pin = 2U;
    xLeds[LED_ACTIVITY].state = LED_OFF;
    
    /* Initialize GPIO pins */
    for (u8Index = 0U; u8Index < LED_COUNT; u8Index++)
    {
        if (xLeds[u8Index].id != LED_NONE)
        {
            HAL_GPIO_Configure(xLeds[u8Index].pin, 1U); /* Output mode */
        }
    }
    
    return bResult;
}

/**
 * @brief Set LED state
 */
bool LED_Set(LedId_t id, LedState_t state)
{
    bool bResult = false;
    
    if ((id > LED_NONE) && (id < LED_COUNT))
    {
        xLeds[id].state = state;
        
        switch (state)
        {
            case LED_OFF:
                xLeds[id].is_on = false;
                HAL_GPIO_Write(xLeds[id].pin, 0U);
                bResult = true;
                break;
                
            case LED_ON:
                xLeds[id].is_on = true;
                HAL_GPIO_Write(xLeds[id].pin, 1U);
                bResult = true;
                break;
                
            case LED_TOGGLE:
                LED_Toggle(id);
                bResult = true;
                break;
                
            case LED_BLINK:
                xLeds[id].state = LED_BLINK;
                bResult = true;
                break;
                
            default:
                break;
        }
    }
    
    return bResult;
}

/**
 * @brief Toggle LED state
 */
bool LED_Toggle(LedId_t id)
{
    bool bResult = false;
    
    if ((id > LED_NONE) && (id < LED_COUNT))
    {
        xLeds[id].is_on = !xLeds[id].is_on;
        HAL_GPIO_Write(xLeds[id].pin, xLeds[id].is_on ? 1U : 0U);
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Update all LEDs (called periodically)
 */
void LED_Update(void)
{
    uint8_t u8Index;
    
    u32SystemTick++;
    
    for (u8Index = 0U; u8Index < LED_COUNT; u8Index++)
    {
        if (xLeds[u8Index].state == LED_BLINK)
        {
            if ((u32SystemTick - xLeds[u8Index].last_toggle_time) >= 
                (xLeds[u8Index].blink_rate_ms / 10U))
            {
                LED_Toggle(xLeds[u8Index].id);
                xLeds[u8Index].last_toggle_time = u32SystemTick;
            }
        }
    }
}

/**
 * @brief Set blink rate for LED
 */
bool LED_SetBlinkRate(LedId_t id, uint32_t rate_ms)
{
    bool bResult = false;
    
    if ((id > LED_NONE) && (id < LED_COUNT))
    {
        xLeds[id].blink_rate_ms = rate_ms;
        bResult = true;
    }
    
    return bResult;
}
