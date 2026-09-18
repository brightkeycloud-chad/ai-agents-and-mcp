# Data Management

## Purpose
This rule ensures proper data handling, privacy, and compliance practices.

## Instructions
- MUST implement data encryption at rest and in transit for all sensitive data. (ID: DATA_ENCRYPTION)
- MUST follow data retention policies and implement automated data lifecycle management. (ID: DATA_RETENTION)
- MUST sanitize and validate all user inputs to prevent injection attacks. (ID: INPUT_VALIDATION)
- MUST implement multi-factor authentication (MFA) for all administrative access. (ID: MFA_REQUIRED)
- MUST rotate credentials regularly and implement automated credential rotation where possible. (ID: CREDENTIAL_ROTATION)

## Priority
Critical

## Error Handling
- If encryption is not available, use access controls and document the security limitation
- If automated rotation is not supported, implement manual rotation procedures and document the process
