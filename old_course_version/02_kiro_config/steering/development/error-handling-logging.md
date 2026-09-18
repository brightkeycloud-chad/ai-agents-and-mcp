# Error Handling and Logging

## Purpose
This rule ensures proper error handling and logging practices are implemented in all code.

## Instructions
- MUST include comprehensive error handling in all code implementations with try-catch blocks, proper exception handling, and graceful failure modes. (ID: ERROR_HANDLING)
- MUST implement structured logging with appropriate log levels (DEBUG, INFO, WARN, ERROR) for debugging, monitoring, and operational visibility. (ID: LOGGING)

## Priority
High

## Error Handling
- If logging framework is not available, use basic console output and document the limitation
- If error handling patterns are inconsistent, follow existing patterns and note inconsistency