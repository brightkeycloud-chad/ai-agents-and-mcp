# Amazon Q Rules Directory

## Overview
This directory contains structured rules for Amazon Q development practices, organized by domain and priority level.

## Rule Structure
Each rule file follows this format:
- **Purpose**: What the rule achieves
- **Instructions**: Specific requirements with unique IDs
- **Priority**: Critical, High, or Medium
- **Error Handling**: Fallback strategies

## Directory Organization
- `api/` - API design and integration standards
- `compliance/` - Governance and regulatory compliance
- `development/` - General development practices
- `documentation/` - Code documentation requirements
- `general/` - Cross-cutting concerns and planning
- `IaC/` - Infrastructure as Code practices
- `monitoring/` - Observability and monitoring
- `resilience/` - Disaster recovery and business continuity
- `security/` - Security and access control

## Rule Dependencies
- `CONSULT_MCP` → All other MCP-specific rules
- `CREATE_PLAN` → All implementation rules
- `LEAST_PRIVILEGE` → All security-related rules
- `USE_DOC_MCP` → `DOCUMENT_APIS`
- `ERROR_HANDLING` → `LOGGING`
- `CHECK_RULES` → All rules depend on this one

## Implementation Phases
### Phase 1: Critical Rules (6 rules) - Must implement first
- Security and access control fundamentals
- MCP consultation requirements
- Planning and approval processes

### Phase 2: High Priority Rules (8 rules) - Core practices
- Development standards and testing
- Infrastructure as code practices
- Error handling and logging

### Phase 3: Medium Priority Rules (4 rules) - Optimization
- Performance optimization
- Cost estimation
- Advanced monitoring

## Rule ID Index
All rule instructions have unique IDs for tracking and reference. Use these IDs when documenting compliance or exceptions.

## Usage
Rules are designed to be:
1. Actionable with clear requirements
2. Measurable with specific criteria
3. Flexible with error handling strategies
4. Traceable with unique identifiers
