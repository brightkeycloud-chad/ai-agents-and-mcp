# Observability

## Purpose
This rule ensures proper monitoring and traceability for all systems and workflows.

## Instructions
- MUST ensure important Key Performance Indicators (KPIs), business metrics, and operational metrics are either logged with structured format or exposed as metrics through monitoring systems. (ID: KPI_MONITORING)
- MUST use consistent tagging, labels, correlation IDs, or trace identifiers to track individual requests, transactions, or workflow executions through distributed systems for observability and debugging. (ID: WORKFLOW_TRACING)
- MUST implement health checks and readiness probes for all services. (ID: HEALTH_CHECKS)
- MUST set up alerting for critical system metrics and business KPIs. (ID: ALERTING)

## Priority
Medium

## Error Handling
- If metrics system is not available, use structured logging and document the limitation
- If tagging/labeling is not supported by the technology, use correlation IDs in logs and document the approach
- If health checks cannot be implemented, use basic service validation and document the monitoring limitation