/**
 * @file task_manager.h
 * @brief Task management header file
 * @details Provides task creation and management interfaces
 */

#ifndef TASK_MANAGER_H
#define TASK_MANAGER_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>
#include "FreeRTOS.h"
#include "task.h"

/**
 * @brief Maximum number of tasks
 */
#define MAX_TASKS   ((uint8_t)10U)

/**
 * @brief Task states
 */
typedef enum
{
    TASK_STATE_IDLE = 0,
    TASK_STATE_READY,
    TASK_STATE_RUNNING,
    TASK_STATE_BLOCKED,
    TASK_STATE_SUSPENDED
} TaskState_t;

/**
 * @brief Task information structure
 */
typedef struct
{
    const char *name;
    TaskHandle_t handle;
    TaskState_t state;
    uint32_t stack_size;
    UBaseType_t priority;
} TaskInfo_t;

/**
 * @brief Initialize task manager
 * @return bool Success status
 */
bool TASK_ManagerInit(void);

/**
 * @brief Get task information
 * @param index Task index
 * @param info Pointer to task info structure
 * @return bool Success status
 */
bool TASK_GetInfo(uint8_t index, TaskInfo_t *info);

/**
 * @brief Get number of active tasks
 * @return uint8_t Number of tasks
 */
uint8_t TASK_GetActiveCount(void);

#ifdef __cplusplus
}
#endif

#endif /* TASK_MANAGER_H */
