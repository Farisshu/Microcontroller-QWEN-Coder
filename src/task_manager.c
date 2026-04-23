/**
 * @file task_manager.c
 * @brief Task manager implementation
 * @details Provides task creation and management functionality
 */

#include "task_manager.h"
#include <string.h>

/**
 * @brief Task registry array
 */
static TaskInfo_t xTaskRegistry[MAX_TASKS];

/**
 * @brief Number of registered tasks
 */
static uint8_t u8TaskCount = 0U;

/**
 * @brief Initialize task manager
 */
bool TASK_ManagerInit(void)
{
    memset(xTaskRegistry, 0, sizeof(xTaskRegistry));
    u8TaskCount = 0U;
    return true;
}

/**
 * @brief Get task information
 */
bool TASK_GetInfo(uint8_t index, TaskInfo_t *info)
{
    bool bResult = false;
    
    if ((index < MAX_TASKS) && (info != NULL))
    {
        memcpy(info, &xTaskRegistry[index], sizeof(TaskInfo_t));
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Get number of active tasks
 */
uint8_t TASK_GetActiveCount(void)
{
    return u8TaskCount;
}
