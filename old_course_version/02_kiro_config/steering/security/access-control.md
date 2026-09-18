# Access Control

## Purpose
This rule ensures secure access control practices and prevents privilege escalation.

## Instructions
- MUST follow the principle of least privilege for all access controls - grant only the minimum permissions required for functionality. (ID: LEAST_PRIVILEGE)
- NEVER grant administrative, root, or wildcard permissions to any resource or service. (ID: NO_ADMIN_PERMISSIONS)
- MUST use temporary credentials, IAM roles, or service accounts instead of long-lived access keys wherever possible. (ID: TEMPORARY_CREDENTIALS)

## Priority
Critical

## Error Handling
- If least privilege cannot be determined, start with minimal permissions and expand as needed
- If temporary credentials are not available, use service accounts with limited scope and document the limitation