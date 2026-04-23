# CI/CD Pipeline Report Summary

**Generated:** 2026-04-23 12:49:41

## Project Information
- **Project:** Microcontroller-QWEN-Coder
- **Branch:** main
- **Commit:** a1b2c3d4

## Overall Status

⚠️ **Status:** passed_with_warnings
**Grade:** A-
**Ready for Production:** No
**Blocking Issues:** 0
**Warnings:** 5

## MISRA C:2012 Compliance

**Compliance Rate:** 94.7%
**Rules Passed:** 134/142

### Violations

- **Rule 5.1** (warning): External identifiers shall be unique
  - File: `src/task_manager.c:45`
- **Rule 8.7** (warning): Functions and objects should not be defined with external linkage if they are referenced in only one translation unit
  - File: `src/utils.c:23`
- **Rule 21.1** (advisory): <stdio.h>, <time.h>, <math.h> shall not be used
  - File: `src/debug_output.c:12`

## Test Results

**Framework:** Unity + CMock
**Total Tests:** 156
**Passed:** 152
**Failed:** 2
**Success Rate:** 97.4%

### Failed Tests

- `test_queue_overflow_handling` in `tests/test_queue_manager.c:234`
  - Error: Expected 1 but was 0
- `test_task_priority_change` in `tests/test_scheduler.c:567`
  - Error: Task state mismatch after priority change

## FreeRTOS Analysis

**Version:** 10.4.6
**Status:** detected

### Task Summary
- Total Tasks: 8
- High Priority: 2
- Medium Priority: 4
- Low Priority: 2

## Build Information

**Compiler:** arm-none-eabi-gcc v12.2.1
**Target:** ARM Cortex-M4F
**Optimization:** -O2

### Binary Size
- Total Size: 29,696 bytes
- Utilization: 45.3%

## Recommendations

### High Priority
- [testing] Increase test coverage for interrupt_handlers module (currently 45.6%)
  - Estimated Effort: 4 hours

### Medium Priority
- [misra] Address MISRA rule 5.1 violation in task_manager.c
  - Estimated Effort: 1 hour
- [code_quality] Fix null pointer dereference warning in message_handler.c
  - Estimated Effort: 2 hours
