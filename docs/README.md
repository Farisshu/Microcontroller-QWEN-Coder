# Microcontroller-QWEN-Coder Documentation

## Overview
This documentation provides comprehensive information about the embedded system project developed using Qwen Coder for research on AI-assisted embedded software development.

## Project Structure

### Source Files (`src/`)
- **main.c** - Main application entry point with FreeRTOS task management
- **system_config.c** - System initialization and message processing
- **task_manager.c** - Task registry and management functionality
- **led_control.c** - LED control implementation with blink support
- **sensor.c** - Sensor reading and calibration functionality
- **hal.c** - Hardware Abstraction Layer for GPIO, UART, and timers

### Header Files (`include/`)
- **system_config.h** - System configuration definitions and types
- **task_manager.h** - Task management interfaces
- **led_control.h** - LED control interfaces
- **sensor.h** - Sensor interfaces and data structures
- **hal.h** - Hardware abstraction interfaces

### Key Features

#### FreeRTOS Integration
- Multi-tasking with 3 application tasks (Main, LED, Sensor)
- Queue-based inter-task communication
- Binary semaphore for resource synchronization
- Stack overflow and malloc failure hooks

#### MISRA C:2012 Compliance
- All code follows MISRA C:2012 guidelines
- Explicit type casting with U-suffix for unsigned literals
- Unused parameters handled with (void) casts
- No implicit conversions
- Defensive programming with null checks

#### Modular Architecture
- Clear separation of concerns
- Hardware abstraction layer
- Reusable component modules
- Well-defined interfaces

## API Reference

### System Configuration
```c
SystemStatus_t SYS_Init(void);
SystemStatus_t SYS_ProcessMessage(const SystemMessage_t *msg);
uint32_t SYS_GetTick(void);
bool SYS_IsInitialized(void);
```

### Task Manager
```c
bool TASK_ManagerInit(void);
bool TASK_GetInfo(uint8_t index, TaskInfo_t *info);
uint8_t TASK_GetActiveCount(void);
```

### LED Control
```c
bool LED_Init(void);
bool LED_Set(LedId_t id, LedState_t state);
bool LED_Toggle(LedId_t id);
void LED_Update(void);
bool LED_SetBlinkRate(LedId_t id, uint32_t rate_ms);
```

### Sensor Interface
```c
bool SENSOR_Init(void);
bool SENSOR_ReadAll(void);
bool SENSOR_GetData(uint8_t index, SensorData_t *data);
bool SENSOR_Calibrate(uint8_t index);
uint8_t SENSOR_GetCount(void);
```

### Hardware Abstraction Layer
```c
bool HAL_Init(void);
bool HAL_GPIO_Configure(uint8_t pin, uint8_t mode);
bool HAL_GPIO_Write(uint8_t pin, uint8_t value);
uint8_t HAL_GPIO_Read(uint8_t pin);
bool HAL_UART_Init(uint32_t baud_rate);
bool HAL_UART_Send(const uint8_t *data, uint16_t length);
uint16_t HAL_UART_Receive(uint8_t *data, uint16_t length);
bool HAL_Timer_Init(uint8_t timer_id, uint32_t period_ms);
bool HAL_Timer_Start(uint8_t timer_id);
bool HAL_Timer_Stop(uint8_t timer_id);
```

## Coding Standards

### Naming Conventions
- Functions: `MODULE_FunctionName` (PascalCase with module prefix)
- Variables: `u8Variable`, `bFlag` (Hungarian notation with type prefix)
- Constants: `CONSTANT_NAME` (UPPER_SNAKE_CASE)
- Types: `TypeName_t` (PascalCase with _t suffix)

### Comment Style
- Doxygen-style comments for all public APIs
- Inline comments for complex logic
- MISRA rule references where applicable

### Error Handling
- All functions return status codes
- Null pointer checks on all pointer parameters
- Range validation on array indices

## Building the Project

### Prerequisites
- ARM GCC toolchain or compatible compiler
- FreeRTOS source files
- CMake or Make build system

### Build Commands
```bash
# Configure build
mkdir build && cd build
cmake ..

# Build project
make

# Run tests
make test

# Generate documentation
make docs
```

## Testing Strategy

### Unit Tests
- Individual module testing
- Mock hardware layer for testing
- Coverage analysis with gcov

### Integration Tests
- Task interaction verification
- Queue communication testing
- Semaphore synchronization testing

### Static Analysis
- cppcheck for general issues
- clang-tidy for modern C++ checks
- MISRA compliance verification

## CI/CD Pipeline

The project includes automated CI/CD via GitHub Actions:
- Code quality checks on every commit
- MISRA compliance verification
- Unit test execution
- Build verification
- Report generation

## License
MIT License - See LICENSE file for details

## Contributing
Please follow the coding standards and ensure all contributions:
1. Pass static analysis
2. Include unit tests
3. Update documentation
4. Follow MISRA guidelines

## Version History
- v1.0.0 - Initial release with core functionality
