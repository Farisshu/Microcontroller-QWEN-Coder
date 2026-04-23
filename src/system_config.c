/**
 * @file system_config.c
 * @brief System configuration implementation
 * @details Contains system-wide initialization and message processing
 */

#include "system_config.h"
#include "hal.h"
#include "sensor.h"
#include "led_control.h"
#include <string.h>

/**
 * @brief System initialized flag
 */
static bool bSystem_Initialized = false;

/**
 * @brief System tick counter
 */
static uint32_t u32System_Tick = 0U;

/**
 * @brief System initialization function
 */
SystemStatus_t SYS_Init(void)
{
    SystemStatus_t eResult = SYS_SUCCESS;
    
    /* Initialize HAL */
    if (!HAL_Init())
    {
        eResult = SYS_ERROR_INIT_FAILED;
    }
    
    /* Initialize LEDs */
    if (eResult == SYS_SUCCESS)
    {
        if (!LED_Init())
        {
            eResult = SYS_ERROR_INIT_FAILED;
        }
    }
    
    /* Initialize sensors */
    if (eResult == SYS_SUCCESS)
    {
        if (!SENSOR_Init())
        {
            eResult = SYS_ERROR_INIT_FAILED;
        }
    }
    
    if (eResult == SYS_SUCCESS)
    {
        bSystem_Initialized = true;
        u32System_Tick = 0U;
    }
    
    return eResult;
}

/**
 * @brief Process system message
 */
SystemStatus_t SYS_ProcessMessage(const SystemMessage_t *msg)
{
    SystemStatus_t eResult = SYS_SUCCESS;
    
    if (msg == NULL)
    {
        eResult = SYS_ERROR_INVALID_PARAM;
    }
    else if (!bSystem_Initialized)
    {
        eResult = SYS_ERROR_RESOURCE_UNAVAILABLE;
    }
    else
    {
        switch (msg->type)
        {
            case MSG_TYPE_NONE:
                /* No action required */
                break;
                
            case MSG_TYPE_SENSOR_UPDATE:
                SENSOR_ReadAll();
                break;
                
            case MSG_TYPE_LED_COMMAND:
                if (msg->data[0] < 4U)
                {
                    LED_Toggle((LedId_t)msg->data[0]);
                }
                break;
                
            case MSG_TYPE_SYSTEM_EVENT:
                u32System_Tick++;
                break;
                
            default:
                eResult = SYS_ERROR_INVALID_PARAM;
                break;
        }
    }
    
    return eResult;
}

/**
 * @brief Get system tick count
 * @return uint32_t Current system tick
 */
uint32_t SYS_GetTick(void)
{
    return u32System_Tick;
}

/**
 * @brief Check if system is initialized
 * @return bool Initialization status
 */
bool SYS_IsInitialized(void)
{
    return bSystem_Initialized;
}
