/**
 * @file system_config.h
 * @brief System configuration header file
 * @details Contains system-wide definitions and configurations
 */

#ifndef SYSTEM_CONFIG_H
#define SYSTEM_CONFIG_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief System status codes (MISRA C:2012 Rule 14.4)
 */
typedef enum
{
    SYS_SUCCESS = 0,
    SYS_ERROR_INIT_FAILED,
    SYS_ERROR_RESOURCE_UNAVAILABLE,
    SYS_ERROR_TIMEOUT,
    SYS_ERROR_INVALID_PARAM
} SystemStatus_t;

/**
 * @brief System message types
 */
typedef enum
{
    MSG_TYPE_NONE = 0,
    MSG_TYPE_SENSOR_UPDATE,
    MSG_TYPE_LED_COMMAND,
    MSG_TYPE_SYSTEM_EVENT
} MessageType_t;

/**
 * @brief System message structure
 */
typedef struct
{
    MessageType_t type;
    uint32_t timestamp;
    uint8_t priority;
    uint8_t data[32U];
} SystemMessage_t;

/**
 * @brief Queue size definition
 */
#define QUEUE_SIZE      ((UBaseType_t)10U)

/**
 * @brief System initialization function
 * @return SystemStatus_t Status code
 */
SystemStatus_t SYS_Init(void);

/**
 * @brief Process system message
 * @param msg Pointer to message structure
 * @return SystemStatus_t Status code
 */
SystemStatus_t SYS_ProcessMessage(const SystemMessage_t *msg);

#ifdef __cplusplus
}
#endif

#endif /* SYSTEM_CONFIG_H */
