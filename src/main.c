/**
 * @file main.c
 * @brief Main application entry point for FreeRTOS-based embedded system
 * @details Demonstrates MISRA C:2012 compliance and FreeRTOS integration
 */

#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"

/* MISRA C:2012 Directive 4.10 - Include standard headers first */
#include <stdio.h>
#include <stdlib.h>

/* Application specific includes */
#include "system_config.h"
#include "task_manager.h"
#include "led_control.h"

/**
 * @brief Stack size definitions (MISRA C:2012 Rule 13.4)
 */
#define MAIN_TASK_STACK_SIZE    ((uint16_t)256U)
#define LED_TASK_STACK_SIZE     ((uint16_t)128U)
#define SENSOR_TASK_STACK_SIZE  ((uint16_t)192U)

/**
 * @brief Task priority definitions (MISRA C:2012 Rule 13.4)
 */
#define MAIN_TASK_PRIORITY      ((UBaseType_t)2U)
#define LED_TASK_PRIORITY       ((UBaseType_t)1U)
#define SENSOR_TASK_PRIORITY    ((UBaseType_t)1U)

/**
 * @brief Queue handle for inter-task communication
 */
static QueueHandle_t xSystemQueue = NULL;

/**
 * @brief Semaphore handle for resource synchronization
 */
static SemaphoreHandle_t xResourceSemaphore = NULL;

/**
 * @brief Main task function
 * @param pvParameters Task parameters (unused)
 */
static void vMainTask(void *pvParameters)
{
    (void)pvParameters; /* MISRA C:2012 Rule 17.2 - Unused parameter */
    
    /* Initialize system components */
    if (SYS_Init() != SYS_SUCCESS)
    {
        /* MISRA C:2012 Rule 15.1 - Empty statement intentional */
        ;
    }
    
    /* Create system queue */
    xSystemQueue = xQueueCreate(QUEUE_SIZE, sizeof(SystemMessage_t));
    
    if (xSystemQueue == NULL)
    {
        /* Queue creation failed */
        for (;;)
        {
            vTaskDelay(portMAX_DELAY);
        }
    }
    
    /* Create binary semaphore */
    xResourceSemaphore = xSemaphoreCreateBinary();
    
    if (xResourceSemaphore != NULL)
    {
        xSemaphoreGive(xResourceSemaphore);
    }
    
    /* Main task loop */
    for (;;)
    {
        SystemMessage_t xMessage;
        
        /* Wait for messages */
        if (xQueueReceive(xSystemQueue, &xMessage, pdMS_TO_TICKS(1000U)) == pdPASS)
        {
            /* Process message */
            SYS_ProcessMessage(&xMessage);
        }
        
        /* Blink status LED */
        LED_Toggle(LED_STATUS);
        
        vTaskDelay(pdMS_TO_TICKS(500U));
    }
}

/**
 * @brief LED control task
 * @param pvParameters Task parameters (unused)
 */
static void vLedTask(void *pvParameters)
{
    (void)pvParameters;
    
    for (;;)
    {
        LED_Update();
        vTaskDelay(pdMS_TO_TICKS(100U));
    }
}

/**
 * @brief Sensor reading task
 * @param pvParameters Task parameters (unused)
 */
static void vSensorTask(void *pvParameters)
{
    (void)pvParameters;
    
    for (;;)
    {
        if (xSemaphoreTake(xResourceSemaphore, portMAX_DELAY) == pdTRUE)
        {
            /* Read sensors with exclusive access */
            SENSOR_ReadAll();
            
            xSemaphoreGive(xResourceSemaphore);
        }
        
        vTaskDelay(pdMS_TO_TICKS(250U));
    }
}

/**
 * @brief Application entry point
 */
int main(void)
{
    BaseType_t xResult;
    
    /* Hardware initialization */
    HAL_Init();
    
    /* Create main task */
    xResult = xTaskCreate(
        vMainTask,
        "MainTask",
        MAIN_TASK_STACK_SIZE,
        NULL,
        MAIN_TASK_PRIORITY,
        NULL
    );
    
    if (xResult != pdPASS)
    {
        /* Task creation failed */
        return -1;
    }
    
    /* Create LED task */
    xResult = xTaskCreate(
        vLedTask,
        "LedTask",
        LED_TASK_STACK_SIZE,
        NULL,
        LED_TASK_PRIORITY,
        NULL
    );
    
    if (xResult != pdPASS)
    {
        return -1;
    }
    
    /* Create sensor task */
    xResult = xTaskCreate(
        vSensorTask,
        "SensorTask",
        SENSOR_TASK_STACK_SIZE,
        NULL,
        SENSOR_TASK_PRIORITY,
        NULL
    );
    
    if (xResult != pdPASS)
    {
        return -1;
    }
    
    /* Start the scheduler */
    vTaskStartScheduler();
    
    /* Should never reach here */
    for (;;)
    {
        ;
    }
}

/**
 * @brief Stack overflow hook
 * @param pxTask Task handle
 * @param pcTaskName Task name
 */
void vApplicationStackOverflowHook(TaskHandle_t pxTask, char *pcTaskName)
{
    (void)pxTask;
    (void)pcTaskName;
    
    /* Stack overflow detected */
    for (;;)
    {
        ;
    }
}

/**
 * @brief Malloc failed hook
 */
void vApplicationMallocFailedHook(void)
{
    /* Memory allocation failed */
    for (;;)
    {
        ;
    }
}
