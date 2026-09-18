# General Development Rules

## Purpose
This rule defines general development practices and workflow standards that apply across all projects and technologies.

## Instructions
- MUST follow consistent naming conventions for all resources, variables, functions, and code elements using descriptive, standardized patterns (camelCase for variables, PascalCase for classes, kebab-case for resources). (ID: NAMING_CONVENTIONS)
- MUST implement comprehensive testing including unit tests, integration tests, and validation tests for all new features and changes. (ID: TESTING)
- MUST use configuration management with environment-specific settings externalized from code using environment variables, config files, or parameter stores. (ID: CONFIG_MANAGEMENT)

## Priority
High

## Error Handling
- If naming conventions conflict with existing code, follow existing patterns and note inconsistency
- If testing framework is not available, document the testing approach and requirements