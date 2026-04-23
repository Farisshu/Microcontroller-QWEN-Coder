/**
 * @file sensor.c
 * @brief Sensor implementation
 * @details Provides sensor reading and management functionality
 */

#include "sensor.h"
#include <string.h>

/**
 * @brief Sensor registry
 */
static SensorData_t xSensors[MAX_SENSORS];

/**
 * @brief Number of available sensors
 */
static uint8_t u8SensorCount = 0U;

/**
 * @brief Initialize sensor subsystem
 */
bool SENSOR_Init(void)
{
    memset(xSensors, 0, sizeof(xSensors));
    
    /* Initialize default sensors */
    xSensors[0].type = SENSOR_TYPE_TEMPERATURE;
    xSensors[0].status = SENSOR_STATUS_OK;
    xSensors[0].value = 2500; /* 25.00 degrees */
    
    xSensors[1].type = SENSOR_TYPE_HUMIDITY;
    xSensors[1].status = SENSOR_STATUS_OK;
    xSensors[1].value = 4500; /* 45.00 percent */
    
    xSensors[2].type = SENSOR_TYPE_PRESSURE;
    xSensors[2].status = SENSOR_STATUS_OK;
    xSensors[2].value = 101325; /* Standard pressure */
    
    u8SensorCount = 3U;
    
    return true;
}

/**
 * @brief Read all sensors
 */
bool SENSOR_ReadAll(void)
{
    uint8_t u8Index;
    
    for (u8Index = 0U; u8Index < u8SensorCount; u8Index++)
    {
        /* Simulate sensor reading */
        xSensors[u8Index].value += 1;
        xSensors[u8Index].timestamp = u8Index;
        
        if (xSensors[u8Index].status == SENSOR_STATUS_OK)
        {
            xSensors[u8Index].calibrated_value = 
                ((float)xSensors[u8Index].value) / 100.0f;
        }
    }
    
    return true;
}

/**
 * @brief Get sensor data by index
 */
bool SENSOR_GetData(uint8_t index, SensorData_t *data)
{
    bool bResult = false;
    
    if ((index < u8SensorCount) && (data != NULL))
    {
        memcpy(data, &xSensors[index], sizeof(SensorData_t));
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Calibrate sensor
 */
bool SENSOR_Calibrate(uint8_t index)
{
    bool bResult = false;
    
    if (index < u8SensorCount)
    {
        xSensors[index].calibrated_value = 
            ((float)xSensors[index].value) / 100.0f;
        xSensors[index].status = SENSOR_STATUS_OK;
        bResult = true;
    }
    
    return bResult;
}

/**
 * @brief Get number of available sensors
 */
uint8_t SENSOR_GetCount(void)
{
    return u8SensorCount;
}
