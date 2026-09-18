# Claude Code Development Rules

## Overview
This document contains structured rules for Claude Code development practices, organized by domain and priority level. The structure mirrors Amazon Q's modular rule system but is consolidated into a single file for Claude Code.

## Rule Structure
Each rule section follows this format:
- **Purpose**: What the rule achieves
- **Instructions**: Specific requirements with unique IDs
- **Priority**: Critical, High, or Medium
- **Error Handling**: Fallback strategies

## Directory Organization (Logical Sections)
- **GLOBAL** - Always active mandatory rules
- **Conversation** - Response formatting and rule citation
- **General** - MCP consultation, planning, error troubleshooting, general development
- **Security** - Access control, data management
- **Compliance** - Governance and security reviews
- **Development** - Error handling, deployment testing, cloud functions, performance, Python, version control
- **Documentation** - Code documentation requirements
- **API** - API design standards
- **IaC** - Infrastructure as Code (Terraform, cost estimation)
- **Monitoring** - Observability and monitoring
- **Resilience** - Disaster recovery

---

# GLOBAL - Always Active Rules

## Purpose
This section contains rules that MUST be applied to every Claude Code interaction regardless of context.

## Instructions
- MANDATORY: Apply all rules from this document at conversation start. (ID: LOAD_ALL_RULES)
- MANDATORY: Check conversation rules for response formatting requirements. (ID: CHECK_CONVERSATION_RULES)
- MANDATORY: Apply security rules for any code or infrastructure work. (ID: APPLY_SECURITY)
- MANDATORY: Apply development rules for any coding tasks. (ID: APPLY_DEVELOPMENT)

## Priority
Critical

## Error Handling
- If specific rules are unclear, ask for clarification
- If conflicting rules apply, follow the highest priority rule and note the conflict

---

# Conversation

## Purpose
This rule defines how Claude Code should behave in ALL conversations and MUST be consulted for every response.

## Instructions
- MANDATORY: Consider rules from this document before EVERY response. (ID: MANDATORY_RULES)
- ALWAYS consider applicable rules before using a tool or responding. (ID: CHECK_RULES)
- MANDATORY: Start with "Rule used: `section_name` (ID) - brief explanation" when applying ANY rule with priority level MANDATORY, CRITICAL, or HIGH. (ID: PRINT_RULES)
- ENFORCEMENT: Rule citation required for all mandatory, critical, and high priority rule applications. (ID: ENFORCE_RULE_PRINTING)
- If multiple rules are matched, list all: "Rule used: `section1` (ID1), `section2` (ID2) - explanation". (ID: PRINT_MULTIPLE)
- Skip rule citation only for medium and low priority rules or purely conversational responses. (ID: SELECTIVE_CITATION)
- DO NOT start responses with generic mentions about using rules or context - be specific about which rules are active. (ID: NO_GENERIC_MENTIONS)

## Priority
Critical

## Error Handling
- If rules are unclear, continue but note the issue
- If multiple conflicting rules apply, follow the highest priority rule and note the conflict

---

# General / MCP Consultation

## Purpose
This rule ensures accuracy by requiring consultation of MCP servers when available for technical specifications and best practices.

## Instructions
- MUST always consult available MCP servers for technical accuracy, best practices, and current specifications before providing recommendations or implementing solutions. (ID: CONSULT_MCP)
- MUST verify information is current, especially for rapidly-evolving technologies, frameworks, and APIs - use MCP servers, WebSearch, or WebFetch as appropriate. (ID: VERIFY_CURRENT)
- When MCP servers are available for a domain (AWS, Terraform, cost estimation, documentation generation, etc.), prioritize them over web search. (ID: MCP_FIRST)

## Priority
Critical

## Error Handling
- If MCP servers are not available, use WebSearch/WebFetch to gather current information and note the limitation

---

# General / Development Planning

## Purpose
This rule ensures systematic planning and validation for all new development or changes.

## Instructions
- MUST use TodoWrite tool to create structured task lists for any non-trivial development work (3+ steps or complex changes). (ID: USE_TODOWRITE)
- MUST structure plans with discrete, measurable steps that can be validated independently. (ID: DISCRETE_STEPS)
- MUST obtain explicit approval of the plan before beginning implementation. (ID: PLAN_APPROVAL)
- MUST include architectural diagrams, flowcharts, or visual representations for complex system interactions. (ID: INCLUDE_DIAGRAMS)
- MUST have exactly one task marked as in_progress at any time. (ID: ONE_IN_PROGRESS)
- MUST mark tasks as completed immediately upon finishing (not batched). (ID: IMMEDIATE_COMPLETION)

## Priority
Critical

## Error Handling
- If TodoWrite is not appropriate for simple tasks, proceed directly but explain approach first
- If diagram tools are not available, use text-based descriptions and document the visual limitation

---

# General / Error Troubleshooting

## Purpose
This rule ensures systematic debugging and troubleshooting when errors are encountered.

## Instructions
- MUST debug systematically when errors occur - analyze error messages, check logs, identify root causes before attempting fixes. (ID: DEBUG_SYSTEMATICALLY)
- MUST use available MCP servers for identifying fixes, solutions, and best practices when troubleshooting errors. (ID: MCP_ERROR_FIXES)
- MUST use WebSearch for error messages, stack traces, and solutions to unfamiliar errors when MCP servers don't cover the domain. (ID: USE_SEARCH_TOOLS)
- MUST read files before editing them (Edit and Write tools require prior Read). (ID: READ_BEFORE_EDIT)
- MUST verify fixes resolve the issue (run tests, check output, validate behavior). (ID: VERIFY_FIXES)

## Priority
High

## Error Handling
- If MCP servers are not available for error resolution, use available debugging tools and WebSearch, then document the limitation
- If error cannot be resolved, document error details and attempted solutions

---

# General / General Development

## Purpose
This rule defines general development practices and workflow standards that apply across all projects and technologies.

## Instructions
- MUST follow language-appropriate naming conventions consistently (camelCase for variables, PascalCase for classes, kebab-case for resources). (ID: NAMING_CONVENTIONS)
- MUST implement comprehensive testing including unit tests, integration tests, and validation tests. (ID: TESTING)
- MUST externalize configuration from code using environment variables, config files, or parameter stores. (ID: CONFIG_MANAGEMENT)
- MUST prefer editing existing files over creating new files unless explicitly required. (ID: PREFER_EDIT)

## Priority
High

## Error Handling
- If naming conventions conflict with existing code, follow existing patterns and note inconsistency
- If testing framework is not available, document the testing approach and requirements

---

# General / Tool Usage Optimization

## Purpose
This rule ensures efficient and appropriate use of Claude Code tools.

## Instructions
- MUST use specialized tools (Read, Edit, Write, Glob, Grep) instead of Bash for file operations. (ID: USE_SPECIALIZED_TOOLS)
- MUST call independent tools in parallel within a single message for optimal performance. (ID: PARALLEL_TOOLS)
- MUST use Task agent with subagent_type=Explore for codebase exploration questions (not needle queries). (ID: EXPLORE_AGENT)
- NEVER use bash echo or commands to communicate with user; output text directly. (ID: NO_BASH_COMMUNICATION)
- MUST quote file paths with spaces in Bash commands. (ID: PROPER_QUOTING)

## Priority
High

## Error Handling
- If preferred tool is not available, use alternatives and explain the approach

---

# Security / Access Control

## Purpose
This rule ensures secure access control practices and prevents privilege escalation.

## Instructions
- MUST follow the principle of least privilege - grant only minimum permissions required. (ID: LEAST_PRIVILEGE)
- NEVER grant administrative, root, or wildcard permissions without explicit user confirmation. (ID: NO_ADMIN_PERMISSIONS)
- MUST use temporary credentials, IAM roles, service accounts, or tokens instead of long-lived access keys. (ID: TEMPORARY_CREDENTIALS)
- NEVER hard-code credentials, API keys, or secrets in source code. (ID: NO_SECRETS_IN_CODE)

## Priority
Critical

## Error Handling
- If least privilege cannot be determined, start with minimal permissions and expand as needed with user approval
- If temporary credentials are not available, use service accounts with limited scope and document the limitation

---

# Security / Data Management

## Purpose
This rule ensures proper data handling, privacy, and security.

## Instructions
- MUST implement data encryption at rest and in transit for all sensitive data. (ID: DATA_ENCRYPTION)
- MUST sanitize and validate all user inputs to prevent injection attacks. (ID: INPUT_VALIDATION)
- MUST implement credential rotation mechanisms where applicable. (ID: CREDENTIAL_ROTATION)
- MUST follow data retention policies and implement automated data lifecycle management. (ID: DATA_RETENTION)
- MUST implement multi-factor authentication (MFA) for all administrative access. (ID: MFA_REQUIRED)
- NEVER create tools for bulk credential discovery or harvesting (SSH keys, browser cookies, cryptocurrency wallets). (ID: NO_CREDENTIAL_HARVESTING)
- Only assist with defensive security tasks; refuse to create malicious code. (ID: DEFENSIVE_SECURITY_ONLY)

## Priority
Critical

## Error Handling
- If encryption is not available for the platform, use access controls and document the security limitation
- If automated rotation is not supported, implement manual rotation procedures and document the process

---

# Compliance / Governance

## Purpose
This rule ensures adherence to regulatory, organizational compliance, and code quality requirements.

## Instructions
- MUST implement audit logging for all administrative actions and data access. (ID: AUDIT_LOGGING)
- MUST conduct security reviews for all code changes involving authentication, authorization, or data access. (ID: SECURITY_REVIEWS)
- NEVER create, modify, or improve code that may be used maliciously. (ID: NO_MALICIOUS_CODE)
- MUST explain security implications when implementing security-sensitive features. (ID: EXPLAIN_SECURITY_IMPACT)

## Priority
Critical

## Error Handling
- If audit logging is not available, implement basic access logging and document the limitation
- If security implications are unclear, research and ask clarifying questions before proceeding

---

# Development / Error Handling and Logging

## Purpose
This rule ensures proper error handling and logging practices are implemented in all code.

## Instructions
- MUST include comprehensive error handling with try-catch blocks, proper exception handling, and graceful failure modes. (ID: ERROR_HANDLING)
- MUST implement structured logging with appropriate log levels (DEBUG, INFO, WARN, ERROR). (ID: LOGGING)
- MUST include relevant context in error messages (what operation failed, input values, expected vs actual). (ID: CONTEXT_IN_ERRORS)

## Priority
High

## Error Handling
- If logging framework is not available, use basic console output and document the limitation
- If error handling patterns are inconsistent, follow existing patterns and note inconsistency

---

# Development / Deployment Testing

## Purpose
This rule ensures complete lifecycle testing and automation for resource provisioning and de-provisioning.

## Instructions
- MUST test both deployment and deletion of resources in the same testing cycle to ensure complete lifecycle functionality. (ID: TEST_DELETION)
- MUST create corresponding de-provisioning automation, teardown procedures, or cleanup processes when creating provisioning automation. (ID: DEPROVISION_AUTOMATION)
- MUST verify cleanup completes successfully and no resources leak. (ID: VERIFY_CLEANUP)

## Priority
High

## Error Handling
- If deletion testing fails, document cleanup issues and provide manual steps
- If de-provisioning automation cannot be created, provide manual cleanup instructions and document the limitation

---

# Development / Cloud Function Development

## Purpose
This rule ensures cloud functions (Lambda, Cloud Functions, Azure Functions, etc.) are developed with proper architecture compatibility.

## Instructions
- MUST test with correct architecture (arm64 for AWS Lambda, etc.). (ID: ARCHITECTURE_COMPATIBILITY)
- MUST ensure Docker images support target architecture. (ID: DOCKER_ARCHITECTURE)
- SHOULD test cloud functions locally before deployment. (ID: LOCAL_TESTING)
- SHOULD optimize for cold start performance. (ID: COLD_START_OPTIMIZATION)

## Priority
Medium

## Error Handling
- If architecture testing is not available locally, document the limitation and test in compatible environment
- If Docker image doesn't support required architecture, use alternative and document the constraint

---

# Development / Performance Optimization

## Purpose
This rule ensures performance considerations are integrated into all development decisions.

## Instructions
- SHOULD consider performance implications for code changes including database queries, API calls, and resource utilization. (ID: PERFORMANCE_ANALYSIS)
- SHOULD implement caching strategies where appropriate. (ID: CACHING_STRATEGY)
- SHOULD profile and benchmark critical code paths when making optimizations. (ID: PERFORMANCE_BENCHMARKING)
- MUST avoid N+1 query problems in database operations. (ID: AVOID_N_PLUS_ONE)

## Priority
High

## Error Handling
- If performance profiling tools are not available, use basic timing measurements and document the limitation
- If caching cannot be implemented, optimize algorithms and document performance constraints

---

# Development / Python Development

## Purpose
This rule ensures Python dependencies are managed in isolated virtual environments.

## Instructions
- MUST use a Python virtual environment located in the project root for all dependency installations. (ID: PYTHON_VENV_REQUIRED)
- MUST create virtual environment with `python3 -m venv venv` if it doesn't exist before installing dependencies. (ID: PYTHON_VENV_CREATE)

## Priority
High

## Error Handling
- If virtual environment creation fails, check Python version compatibility and disk space
- If activation fails, verify shell compatibility and provide alternative activation commands

---

# Development / Version Control

## Purpose
This rule ensures consistent version control practices and commit standards.

## Instructions
- MUST write clear, descriptive commit messages following conventional commit format when possible. (ID: COMMIT_MESSAGES)
- MUST use heredoc for multi-line commit messages to ensure proper formatting. (ID: COMMIT_FORMAT)
- MUST include "Co-Authored-By: Claude <noreply@anthropic.com>" in commits. (ID: INCLUDE_COAUTHOR)
- MUST include "🤖 Generated with [Claude Code](https://claude.com/claude-code)" in commits. (ID: INCLUDE_SIGNATURE)
- MUST commit changes when user mentions "checkpointing" or similar requests. (ID: CHECKPOINT_COMMIT)
- NEVER run force push to main/master without explicit user request and warning. (ID: NEVER_FORCE_PUSH)
- NEVER skip git hooks unless explicitly requested. (ID: NO_SKIP_HOOKS)

## Priority
Medium

## Error Handling
- If commit message format conflicts with project standards, follow project standards and note inconsistency

---

# Documentation / Code Documentation

## Purpose
This rule ensures comprehensive documentation is generated for all code using automated tools when available.

## Instructions
- MUST use code documentation generation MCP server for automated documentation when available. (ID: USE_DOC_MCP)
- MUST document all public APIs, interfaces, and complex business logic with clear descriptions, parameters, return values, and usage examples. (ID: DOCUMENT_APIS)
- SHOULD add comments for non-obvious logic, algorithms, or business rules. (ID: CODE_COMMENTS)
- SHOULD include file_path:line_number references when discussing specific code locations. (ID: INCLUDE_REFERENCES)
- NEVER proactively create documentation files (*.md, README) unless explicitly requested. (ID: NO_PROACTIVE_DOCS)

## Priority
High

## Error Handling
- If code documentation generation MCP server is not available, create manual documentation and flag for automation
- If documentation is missing, create basic documentation and flag for improvement

---

# API / Design Standards

## Purpose
This rule ensures consistent and robust API design practices.

## Instructions
- SHOULD implement API versioning strategies to maintain backward compatibility. (ID: API_VERSIONING)
- MUST use standard HTTP status codes and error response formats. (ID: HTTP_STANDARDS)
- SHOULD implement rate limiting and throttling for public APIs. (ID: RATE_LIMITING)
- MUST document API endpoints with request/response examples. (ID: API_DOCUMENTATION)

## Priority
High

## Error Handling
- If versioning cannot be implemented, document API changes and maintain compatibility
- If rate limiting is not available, implement basic request validation and document the limitation

---

# IaC / Infrastructure as Code

## Purpose
This rule ensures consistent Infrastructure as Code practices (Terraform, CloudFormation, etc.).

## Instructions
- MUST use modules/reusable components to promote code reusability. (ID: USE_MODULES)
- MUST use variables instead of hard-coding values, with proper descriptions and types. (ID: USE_VARIABLES)
- MUST use data sources/lookups instead of variables for dynamic values. (ID: USE_DATA_SOURCES)
- MUST use current, supported versions with version constraints - consult MCP servers for current versions. (ID: CURRENT_PROVIDERS)
- MUST run formatting tools (terraform fmt, etc.) before commits. (ID: FORMAT_BEFORE_COMMIT)
- SHOULD implement remote state management with locking for team environments. (ID: STATE_MANAGEMENT)
- MUST validate and preview changes before applying. (ID: VALIDATE_PLAN)
- MUST use the latest stable provider version, and verify this with MCP (ID: PROVIDER_VERSION)

## Priority
High

## Error Handling
- If modules are not available, create reusable components and document for future extraction
- If data sources cannot be used, use variables and document the limitation
- If formatting fails, fix issues before proceeding with commit
- If remote state is not available, use local state and document the collaboration limitation

---

# IaC / Cost Estimation

## Purpose
This rule ensures cost analysis is performed for all proposed infrastructure resources.

## Instructions
- SHOULD generate detailed cost estimates for proposed resources including both static costs (fixed monthly charges) and dynamic costs (usage-based charges) with realistic usage examples. (ID: COST_ESTIMATES)
- SHOULD use cost estimation MCP servers when available for accurate pricing. (ID: USE_COST_MCP)
- SHOULD use web resources, pricing calculators, or documentation when dedicated cost estimation MCP is not available. (ID: WEB_COST_RESOURCES)
- SHOULD suggest cost optimization opportunities when appropriate. (ID: COST_OPTIMIZATION)

## Priority
Medium

## Error Handling
- If cost estimation tools are not available, provide general cost guidance and recommend manual calculation
- If dynamic cost examples cannot be determined, focus on static costs and document the limitation

---

# Monitoring / Observability

## Purpose
This rule ensures proper monitoring and traceability for all systems and workflows.

## Instructions
- SHOULD ensure important KPIs, business metrics, and operational metrics are logged or exposed. (ID: KPI_MONITORING)
- SHOULD use correlation IDs, trace IDs, or labels to track requests through distributed systems. (ID: WORKFLOW_TRACING)
- SHOULD implement health checks and readiness probes for services. (ID: HEALTH_CHECKS)
- SHOULD recommend alerting for critical system metrics. (ID: ALERTING)

## Priority
Medium

## Error Handling
- If metrics system is not available, use structured logging and document the limitation
- If tagging/labeling is not supported, use correlation IDs in logs and document the approach
- If health checks cannot be implemented, use basic service validation and document the monitoring limitation

---

# Resilience / Disaster Recovery

## Purpose
This rule ensures systems are designed for resilience and recovery.

## Instructions
- MUST implement backup strategies for all critical data and configurations. (ID: BACKUP_STRATEGY)
- SHOULD design for multi-AZ or multi-region deployment where business continuity is required. (ID: MULTI_AZ_DESIGN)
- SHOULD document and test disaster recovery procedures. (ID: DR_TESTING)

## Priority
High

## Error Handling
- If multi-AZ deployment is not available, implement single-AZ with documented recovery procedures
- If automated backup is not supported, implement manual backup procedures and document the process

---

# Rule Dependencies

Understanding rule dependencies ensures proper implementation order:

- **CHECK_RULES** → All other rules (ensures rule awareness before action)
- **CONSULT_MCP** → All MCP-specific rules (foundation for technical accuracy)
- **USE_TODOWRITE** → Complex multi-step tasks (planning before execution)
- **LEAST_PRIVILEGE** → All security-related rules (security foundation)
- **USE_SPECIALIZED_TOOLS** → All file operations (efficiency)
- **READ_BEFORE_EDIT** → All file editing operations (tool requirement)
- **ERROR_HANDLING** → **LOGGING** (error handling requires logging)
- **EXPLORE_AGENT** → Codebase exploration (use right tool for the job)
- **USE_DOC_MCP** → **DOCUMENT_APIS** (automated documentation flow)
- **MCP_ERROR_FIXES** → Error troubleshooting (use MCP servers for solutions)

---

# Quick Reference Index

## By Priority Level

### Critical Rules
- **GLOBAL**: LOAD_ALL_RULES, CHECK_CONVERSATION_RULES, APPLY_SECURITY, APPLY_DEVELOPMENT
- **Conversation**: MANDATORY_RULES, CHECK_RULES, PRINT_RULES, ENFORCE_RULE_PRINTING, PRINT_MULTIPLE
- **MCP Consultation**: CONSULT_MCP, VERIFY_CURRENT, MCP_FIRST
- **Development Planning**: USE_TODOWRITE, DISCRETE_STEPS, PLAN_APPROVAL, INCLUDE_DIAGRAMS, ONE_IN_PROGRESS, IMMEDIATE_COMPLETION
- **Access Control**: LEAST_PRIVILEGE, NO_ADMIN_PERMISSIONS, TEMPORARY_CREDENTIALS, NO_SECRETS_IN_CODE
- **Data Management**: DATA_ENCRYPTION, INPUT_VALIDATION, CREDENTIAL_ROTATION, DATA_RETENTION, MFA_REQUIRED, NO_CREDENTIAL_HARVESTING, DEFENSIVE_SECURITY_ONLY
- **Compliance**: AUDIT_LOGGING, SECURITY_REVIEWS, NO_MALICIOUS_CODE, EXPLAIN_SECURITY_IMPACT

### High Priority Rules
- **Error Troubleshooting**: DEBUG_SYSTEMATICALLY, MCP_ERROR_FIXES, USE_SEARCH_TOOLS, READ_BEFORE_EDIT, VERIFY_FIXES
- **General Development**: NAMING_CONVENTIONS, TESTING, CONFIG_MANAGEMENT, PREFER_EDIT
- **Tool Usage**: USE_SPECIALIZED_TOOLS, PARALLEL_TOOLS, EXPLORE_AGENT, NO_BASH_COMMUNICATION, PROPER_QUOTING
- **Error Handling & Logging**: ERROR_HANDLING, LOGGING, CONTEXT_IN_ERRORS
- **Deployment Testing**: TEST_DELETION, DEPROVISION_AUTOMATION, VERIFY_CLEANUP
- **Performance**: PERFORMANCE_ANALYSIS, CACHING_STRATEGY, PERFORMANCE_BENCHMARKING, AVOID_N_PLUS_ONE
- **Python Development**: PYTHON_VENV_REQUIRED, PYTHON_VENV_CREATE
- **Code Documentation**: USE_DOC_MCP, DOCUMENT_APIS, CODE_COMMENTS, INCLUDE_REFERENCES, NO_PROACTIVE_DOCS
- **API Design**: API_VERSIONING, HTTP_STANDARDS, RATE_LIMITING, API_DOCUMENTATION
- **IaC**: USE_MODULES, USE_VARIABLES, USE_DATA_SOURCES, CURRENT_PROVIDERS, FORMAT_BEFORE_COMMIT, STATE_MANAGEMENT, VALIDATE_PLAN
- **Disaster Recovery**: BACKUP_STRATEGY, MULTI_AZ_DESIGN, DR_TESTING

### Medium Priority Rules
- **Version Control**: COMMIT_MESSAGES, COMMIT_FORMAT, INCLUDE_COAUTHOR, INCLUDE_SIGNATURE, CHECKPOINT_COMMIT, NEVER_FORCE_PUSH, NO_SKIP_HOOKS
- **Cloud Functions**: ARCHITECTURE_COMPATIBILITY, DOCKER_ARCHITECTURE, LOCAL_TESTING, COLD_START_OPTIMIZATION
- **Cost Estimation**: COST_ESTIMATES, USE_COST_MCP, WEB_COST_RESOURCES, COST_OPTIMIZATION
- **Observability**: KPI_MONITORING, WORKFLOW_TRACING, HEALTH_CHECKS, ALERTING

## By Domain

### Conversation & Rule Awareness
- MANDATORY_RULES, CHECK_RULES, PRINT_RULES, ENFORCE_RULE_PRINTING, PRINT_MULTIPLE, SELECTIVE_CITATION, NO_GENERIC_MENTIONS

### Planning & Task Management
- USE_TODOWRITE, DISCRETE_STEPS, PLAN_APPROVAL, INCLUDE_DIAGRAMS, ONE_IN_PROGRESS, IMMEDIATE_COMPLETION

### Security
- LEAST_PRIVILEGE, NO_ADMIN_PERMISSIONS, TEMPORARY_CREDENTIALS, NO_SECRETS_IN_CODE, DATA_ENCRYPTION, INPUT_VALIDATION, CREDENTIAL_ROTATION, DATA_RETENTION, MFA_REQUIRED, NO_CREDENTIAL_HARVESTING, DEFENSIVE_SECURITY_ONLY

### Compliance
- AUDIT_LOGGING, SECURITY_REVIEWS, NO_MALICIOUS_CODE, EXPLAIN_SECURITY_IMPACT

### Development Workflow
- NAMING_CONVENTIONS, TESTING, CONFIG_MANAGEMENT, PREFER_EDIT, ERROR_HANDLING, LOGGING, CONTEXT_IN_ERRORS, DEBUG_SYSTEMATICALLY, VERIFY_FIXES

### Infrastructure & Deployment
- USE_MODULES, USE_VARIABLES, USE_DATA_SOURCES, CURRENT_PROVIDERS, FORMAT_BEFORE_COMMIT, STATE_MANAGEMENT, VALIDATE_PLAN, TEST_DELETION, DEPROVISION_AUTOMATION, VERIFY_CLEANUP

### Cloud & Architecture
- ARCHITECTURE_COMPATIBILITY, DOCKER_ARCHITECTURE, LOCAL_TESTING, COLD_START_OPTIMIZATION, BACKUP_STRATEGY, MULTI_AZ_DESIGN, DR_TESTING

### API & Performance
- API_VERSIONING, HTTP_STANDARDS, RATE_LIMITING, API_DOCUMENTATION, PERFORMANCE_ANALYSIS, CACHING_STRATEGY, PERFORMANCE_BENCHMARKING, AVOID_N_PLUS_ONE

### Documentation & Communication
- USE_DOC_MCP, DOCUMENT_APIS, CODE_COMMENTS, INCLUDE_REFERENCES, NO_PROACTIVE_DOCS

### Operations
- KPI_MONITORING, WORKFLOW_TRACING, HEALTH_CHECKS, ALERTING, COST_ESTIMATES, USE_COST_MCP, WEB_COST_RESOURCES, COST_OPTIMIZATION

### Tool Usage
- USE_SPECIALIZED_TOOLS, PARALLEL_TOOLS, EXPLORE_AGENT, NO_BASH_COMMUNICATION, PROPER_QUOTING, READ_BEFORE_EDIT

### MCP & Research
- CONSULT_MCP, VERIFY_CURRENT, MCP_FIRST, MCP_ERROR_FIXES, USE_SEARCH_TOOLS, USE_DOC_MCP, USE_COST_MCP

---

# Implementation Guidelines for Common Tasks

## For All Conversations and Responses
1. Use **CHECK_RULES** before using tools or responding
2. Use **PRINT_RULES** to cite specific rules being followed (e.g., "Rule used: `MCP Consultation` (CONSULT_MCP)")
3. Use **PRINT_MULTIPLE** to list all applicable rules if multiple apply
4. Avoid generic mentions per **NO_GENERIC_MENTIONS** - be specific

## For All New Development
1. Use **CONSULT_MCP** to verify current best practices
2. Use **USE_TODOWRITE** for complex work (3+ steps)
3. Mark tasks **in_progress** one at a time (**ONE_IN_PROGRESS**)
4. Follow **LEAST_PRIVILEGE** and **NO_SECRETS_IN_CODE**
5. Implement **ERROR_HANDLING** and **LOGGING**
6. Create **TESTING** for new features
7. Use **USE_DOC_MCP** or **DOCUMENT_APIS** for public interfaces
8. Write **COMMIT_MESSAGES** with **INCLUDE_COAUTHOR** and **INCLUDE_SIGNATURE**

## For Codebase Exploration
1. Use **EXPLORE_AGENT** (Task with subagent_type=Explore) for:
   - "How does authentication work?"
   - "What is the codebase structure?"
   - "Where are errors handled?"
2. Use **Glob** for finding files by pattern
3. Use **Grep** for finding code/text
4. Use **Read** for examining files
5. Use **PARALLEL_TOOLS** to read multiple files at once

## For File Operations
1. Use **Glob** to find files (not `find` or `ls`)
2. Use **Grep** to search content (not `grep` or `rg` via Bash)
3. Use **Read** to read files (not `cat`/`head`/`tail`)
4. Use **Edit** to modify files (not `sed`/`awk`)
5. Use **Write** to create files (not `echo >`)
6. Remember **READ_BEFORE_EDIT** - must Read before Edit/Write

## For Infrastructure Changes
1. Use **USE_TODOWRITE** for planning
2. Use **CONSULT_MCP** for current provider docs
3. Follow **USE_MODULES**, **USE_VARIABLES**, **USE_DATA_SOURCES**, **CURRENT_PROVIDERS**
4. Test **TEST_DELETION** and create **DEPROVISION_AUTOMATION**
5. Generate **COST_ESTIMATES** using **USE_COST_MCP**
6. Implement **KPI_MONITORING** and **HEALTH_CHECKS**
7. Run **FORMAT_BEFORE_COMMIT**
8. Use **VALIDATE_PLAN** before applying

## For API Development
1. Use **HTTP_STANDARDS** for status codes
2. Implement **INPUT_VALIDATION** for all inputs
3. Consider **API_VERSIONING** for public APIs
4. Implement **RATE_LIMITING** if public
5. Use **WORKFLOW_TRACING** with correlation IDs
6. Create **API_DOCUMENTATION** with examples
7. Avoid **AVOID_N_PLUS_ONE** database issues

## For Debugging/Troubleshooting
1. Follow **DEBUG_SYSTEMATICALLY**
2. Use **MCP_ERROR_FIXES** for solutions
3. Use **USE_SEARCH_TOOLS** for unfamiliar errors
4. Check logs and error messages
5. Ensure **CONTEXT_IN_ERRORS**
6. **VERIFY_FIXES** after changes

## For Git Operations
1. Use **COMMIT_FORMAT** with heredoc
2. Include **INCLUDE_COAUTHOR** and **INCLUDE_SIGNATURE**
3. Follow **CHECKPOINT_COMMIT** when requested
4. Never **NEVER_FORCE_PUSH** to main/master
5. Never **NO_SKIP_HOOKS** unless requested

## For Python Development
1. Use **PYTHON_VENV_REQUIRED** for all projects
2. Create with **PYTHON_VENV_CREATE** if missing
3. Install dependencies in virtual environment

---

# Claude Code-Specific Best Practices

## Understanding MCP Servers vs Claude Code Tools

### MCP Servers (Model Context Protocol)
- Knowledge and consultation endpoints
- Examples: AWS docs, Terraform docs, cost estimation, code documentation
- Use for: Best practices, specifications, pricing, documentation generation
- When: Before implementation, unfamiliar tech, cost estimates, troubleshooting

### Claude Code Tools
- File and codebase operations
- Examples: Read, Write, Edit, Glob, Grep, Bash, Task agents
- Use for: File operations, code searching, codebase exploration, commands
- When: Working with files, searching code, running builds/tests

**Key Principle**: MCP servers for **knowledge**, Claude Code tools for **operations**

## Task Agent Usage
- Use **Explore agent** for codebase exploration ("quick", "medium", "very thorough")
- Use **general-purpose agent** for complex multi-step tasks
- Launch agents in **parallel** when independent
- Provide detailed prompts with expected return information

## Tool Efficiency
- **PARALLEL_TOOLS**: Multiple independent calls in single message
- Read multiple files simultaneously
- Use Glob patterns like `**/*.ts`
- Use Grep with `output_mode: "files_with_matches"` for speed

## Context Management
- Use specialized tools to reduce context
- Use Task agents for extensive exploration
- Reference code as **file_path:line_number** (**INCLUDE_REFERENCES**)

## Security Constraints
- **DEFENSIVE_SECURITY_ONLY**: Only defensive security assistance
- **NO_CREDENTIAL_HARVESTING**: No bulk credential discovery
- **NO_MALICIOUS_CODE**: No malicious code creation/improvement
- Can analyze code, write reports, explain vulnerabilities

---

# Differences from Amazon Q Rules

## Preserved from Amazon Q
- MCP server consultation (CRITICAL priority)
- All MCP-specific rules (CONSULT_MCP, MCP_ERROR_FIXES, USE_DOC_MCP, USE_COST_MCP)
- Domain organization (General, Security, Development, IaC, etc.)
- Rule structure (Purpose, Instructions, Priority, Error Handling)

## Removed/Modified
- "Ultrathink" → TodoWrite
- AWS-specific tagging → Removed (too narrow)
- AWS-specific terminology → Technology-agnostic

## Added for Claude Code
- TodoWrite workflow (USE_TODOWRITE, ONE_IN_PROGRESS, IMMEDIATE_COMPLETION)
- Tool selection (Read/Write/Edit/Glob/Grep/Bash/Task)
- Parallel execution (PARALLEL_TOOLS)
- Task agent patterns (EXPLORE_AGENT)
- Context management strategies
- Security constraints (DEFENSIVE_SECURITY_ONLY, NO_CREDENTIAL_HARVESTING)
- Git commit requirements (INCLUDE_COAUTHOR, INCLUDE_SIGNATURE)
- File preferences (USE_SPECIALIZED_TOOLS, PREFER_EDIT)
- MCP vs Tools distinction

## Adapted
- Planning: ultrathink → TodoWrite
- Examples: AWS-focused → Technology-agnostic
- Workflow: Amazon Q → Claude Code

---

# Usage Notes

- All instructions have unique IDs for tracking
- Rules are actionable, measurable, flexible, and traceable
- Reference rule IDs when documenting compliance/exceptions
- Use as comprehensive development checklist
- Adapt error handling to project constraints
- Maintain security standards for CRITICAL rules
- Prioritize: CRITICAL > HIGH > MEDIUM
