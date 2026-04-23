/**
 * @file hal.h
 * @brief Hardware Abstraction Layer header file
 * @details Provides hardware abstraction for embedded system
 */

#ifndef HAL_H
#define HAL_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Initialize hardware abstraction layer
 * @return bool Success status
 */
bool HAL_Init(void);

/**
 * @brief Configure GPIO pins
 * @param pin Pin number
 * @param mode Pin mode (input/output)
 * @return bool Success status
 */
bool HAL_GPIO_Configure(uint8_t pin, uint8_t mode);

/**
 * @brief Write to GPIO pin
 * @param pin Pin number
 * @param value Value to write (0 or 1)
 * @return bool Success status
 */
bool HAL_GPIO_Write(uint8_t pin, uint8_t value);

/**
 * @brief Read from GPIO pin
 * @param pin Pin number
 * @return uint8_t Pin value
 */
uint8_t HAL_GPIO_Read(uint8_t pin);

/**
 * @brief Initialize UART peripheral
 * @param baud_rate Baud rate
 * @return bool Success status
 */
bool HAL_UART_Init(uint32_t baud_rate);

/**
 * @brief Send data via UART
 * @param data Pointer to data buffer
 * @param length Data length
 * @return bool Success status
 */
bool HAL_UART_Send(const uint8_t *data, uint16_t length);

/**
 * @brief Receive data via UART
 * @param data Pointer to data buffer
 * @param length Maximum length to receive
 * @return uint16_t Number of bytes received
 */
uint16_t HAL_UART_Receive(uint8_t *data, uint16_t length);

/**
 * @brief Initialize timer
 * @param timer_id Timer identifier
 * @param period_ms Period in milliseconds
 * @return bool Success status
 */
bool HAL_Timer_Init(uint8_t timer_id, uint32_t period_ms);

/**
 * @brief Start timer
 * @param timer_id Timer identifier
 * @return bool Success status
 */
bool HAL_Timer_Start(uint8_t timer_id);

/**
 * @brief Stop timer
 * @param timer_id Timer identifier
 * @return bool Success status
 */
bool HAL_Timer_Stop(uint8_t timer_id);

#ifdef __cplusplus
}
#endif

#endif /* HAL_H */
