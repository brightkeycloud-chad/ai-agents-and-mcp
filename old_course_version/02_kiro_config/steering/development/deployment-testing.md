# Deployment Testing

## Purpose
This rule ensures complete lifecycle testing and automation for resource provisioning and de-provisioning.

## Instructions
- MUST test both deployment and deletion of resources in the same testing cycle to ensure complete lifecycle functionality and prevent resource leaks. (ID: TEST_DELETION)
- MUST create corresponding de-provisioning automation scripts, teardown procedures, or cleanup processes when creating any provisioning automation. (ID: DEPROVISION_AUTOMATION)

## Priority
High

## Error Handling
- If deletion testing fails, document the cleanup issues and manual steps required
- If de-provisioning automation cannot be created, provide manual cleanup instructions and document the limitation