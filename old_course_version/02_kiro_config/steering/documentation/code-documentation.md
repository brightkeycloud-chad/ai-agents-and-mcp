# Code Documentation

## Purpose
This rule ensures comprehensive documentation is generated for all code using automated tools when available.

## Instructions
- MUST use the code documentation generation MCP server for automated documentation when available. (ID: USE_DOC_MCP)
- MUST document all public APIs, interfaces, and complex business logic with clear descriptions, parameters, return values, and usage examples. (ID: DOCUMENT_APIS)

## Priority
High

## Error Handling
- If code documentation generation MCP server is not available, create manual documentation and flag for automation
- If documentation is missing, create basic documentation and flag for improvement