/**
 * @file hal.c
 * @brief Hardware Abstraction Layer implementation
 * @details Provides hardware abstraction for embedded system
 */

#include "hal.h"
#include <string.h>

/**
 * @brief GPIO pin configuration structure
 */
typedef struct
{
    uint8_t pin;
    uint8_t mode;
    uint8_t value;
} GPIO_Config_t;

/**
 * @brief GPIO registry
 */
static GPIO_Config_t xGPIO_Pins[32];

/**
 * @brief UART initialized flag
 */
static bool bUART_Initialized = false;

/**
 * @brief Timer configurations
 */
static bool abTimers_Active[8] = {false, false, false, false, false, false, false, false};

/**
 * @brief Initialize hardware abstraction layer
 */
bool HAL_Init(void)
{
    memset(xGPIO_Pins, 0, sizeof(xGPIO_Pins));
    bUART_Initialized = false;
    memset(abTimers_Active, 0, sizeof(abTimers_Active));
    
    return true;
}

/**
 * @brief Configure GPIO pins
 */
bool HAL_GPIO_Configure(uint8_t pin, uint8_t mode)
{
    bool bResult = false;
    
    if (pin < 32U)
    {
        xGPIO_Pins[pin].pin = pin;
        xGPIO_Pins[pin].mode = mode;
        xGPIO_Pins[pin].value = 0U;
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Write to GPIO pin
 */
bool HAL_GPIO_Write(uint8_t pin, uint8_t value)
{
    bool bResult = false;
    
    if ((pin < 32U) && (xGPIO_Pins[pin].mode == 1U))
    {
        xGPIO_Pins[pin].value = value & 1U;
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Read from GPIO pin
 */
uint8_t HAL_GPIO_Read(uint8_t pin)
{
    uint8_t u8Result = 0U;
    
    if (pin < 32U)
    {
        u8Result = xGPIO_Pins[pin].value;
    }
    
    return u8Result;
}

/**
 * @brief Initialize UART peripheral
 */
bool HAL_UART_Init(uint32_t baud_rate)
{
    (void)baud_rate; /* MISRA C:2012 Rule 17.2 - Unused parameter in simulation */
    
    bUART_Initialized = true;
    return true;
}

/**
 * @brief Send data via UART
 */
bool HAL_UART_Send(const uint8_t *data, uint16_t length)
{
    bool bResult = false;
    
    if ((data != NULL) && (length > 0U) && bUART_Initialized)
    {
        /* Simulate UART transmission */
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Receive data via UART
 */
uint16_t HAL_UART_Receive(uint8_t *data, uint16_t length)
{
    uint16_t u16Received = 0U;
    
    if ((data != NULL) && (length > 0U) && bUART_Initialized)
    {
        /* Simulate UART reception - no data available */
        u16Received = 0U;
    }
    
    return u16Received;
}

/**
 * @brief Initialize timer
 */
bool HAL_Timer_Init(uint8_t timer_id, uint32_t period_ms)
{
    bool bResult = false;
    
    (void)period_ms; /* MISRA C:2012 Rule 17.2 - Unused parameter in simulation */
    
    if (timer_id < 8U)
    {
        abTimers_Active[timer_id] = false;
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Start timer
 */
bool HAL_Timer_Start(uint8_t timer_id)
{
    bool bResult = false;
    
    if (timer_id < 8U)
    {
        abTimers_Active[timer_id] = true;
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Stop timer
 */
bool HAL_Timer_Stop(uint8_t timer_id)
{
    bool bResult = false;
    
    if (timer_id < 8U)
    {
        abTimers_Active[timer_id] = false;
        bResult = true;
    }
    
    return bResult;
}
