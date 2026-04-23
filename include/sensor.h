/**
 * @file sensor.h
 * @brief Sensor interface header file
 * @details Provides sensor reading and management interfaces
 */

#ifndef SENSOR_H
#define SENSOR_H

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

/**
 * @brief Maximum number of sensors
 */
#define MAX_SENSORS     ((uint8_t)8U)

/**
 * @brief Sensor types
 */
typedef enum
{
    SENSOR_TYPE_NONE = 0,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPE_HUMIDITY,
    SENSOR_TYPE_PRESSURE,
    SENSOR_TYPE_ACCELEROMETER,
    SENSOR_TYPE_GYROSCOPE
} SensorType_t;

/**
 * @brief Sensor status codes
 */
typedef enum
{
    SENSOR_STATUS_OK = 0,
    SENSOR_STATUS_ERROR,
    SENSOR_STATUS_NOT_READY,
    SENSOR_STATUS_CALIBRATION_REQUIRED
} SensorStatus_t;

/**
 * @brief Sensor data structure
 */
typedef struct
{
    SensorType_t type;
    SensorStatus_t status;
    int32_t value;
    uint32_t timestamp;
    float calibrated_value;
} SensorData_t;

/**
 * @brief Initialize sensor subsystem
 * @return bool Success status
 */
bool SENSOR_Init(void);

/**
 * @brief Read all sensors
 * @return bool Success status
 */
bool SENSOR_ReadAll(void);

/**
 * @brief Get sensor data by index
 * @param index Sensor index
 * @param data Pointer to sensor data structure
 * @return bool Success status
 */
bool SENSOR_GetData(uint8_t index, SensorData_t *data);

/**
 * @brief Calibrate sensor
 * @param index Sensor index
 * @return bool Success status
 */
bool SENSOR_Calibrate(uint8_t index);

/**
 * @brief Get number of available sensors
 * @return uint8_t Number of sensors
 */
uint8_t SENSOR_GetCount(void);

#ifdef __cplusplus
}
#endif

#endif /* SENSOR_H */
