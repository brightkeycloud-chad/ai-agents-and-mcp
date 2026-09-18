# Disaster Recovery

## Purpose
This rule ensures systems are designed for resilience and recovery.

## Instructions
- MUST implement backup strategies for all critical data and configurations. (ID: BACKUP_STRATEGY)
- MUST design for multi-AZ or multi-region deployment where business continuity is required. (ID: MULTI_AZ_DESIGN)
- MUST document and test disaster recovery procedures. (ID: DR_TESTING)

## Priority
High

## Error Handling
- If multi-AZ deployment is not available, implement single-AZ with documented recovery procedures
- If automated backup is not supported, implement manual backup procedures and document the process
