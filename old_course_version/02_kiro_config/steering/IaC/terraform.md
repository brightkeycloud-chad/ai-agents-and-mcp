# Terraform Infrastructure as Code

## Purpose
This rule ensures consistent Terraform practices and code quality standards.

## Instructions
- MUST use Terraform modules wherever possible to promote code reusability, maintainability, and consistency across projects. (ID: USE_MODULES)
- MUST use variables instead of hard-coding values, with proper variable descriptions, types, and default values where appropriate. (ID: USE_VARIABLES)
- MUST use data sources instead of variables for dynamic lookups of existing resources, AMIs, availability zones, and other runtime-determined values. (ID: USE_DATA_OBJECTS)
- MUST use current, supported versions of Terraform providers and specify version constraints to ensure compatibility. (ID: CURRENT_PROVIDERS)
- MUST execute `terraform fmt` before any code commit to ensure consistent formatting and style. (ID: TERRAFORM_FMT)
- MUST implement remote state management with state locking to prevent concurrent modifications. (ID: REMOTE_STATE)
- MUST use terraform validate and terraform plan before any apply operations. (ID: VALIDATE_PLAN)
- MUST use the latest stable provider version, and verify this with MCP (ID: PROVIDER_VERSION)

## Priority
High

## Error Handling
- If modules are not available, create reusable resources and document for future module extraction
- If data objects cannot be used, use variables and document the limitation
- If terraform fmt fails, fix formatting issues before proceeding with commit
- If remote state is not available, use local state and document the collaboration limitation
