# Compliance

## Purpose
This rule ensures adherence to regulatory and organizational compliance requirements.

## Instructions
- MUST implement audit logging for all administrative actions and data access. (ID: AUDIT_LOGGING)
- MUST follow organizational tagging standards for all AWS resources. (ID: RESOURCE_TAGGING)
- MUST conduct security reviews for all code changes involving sensitive operations. (ID: SECURITY_REVIEWS)

## Priority
Critical

## Error Handling
- If audit logging is not available, implement basic access logging and document the limitation
- If tagging standards are not defined, use basic resource identification and document the approach
