# API Design

## Purpose
This rule ensures consistent and robust API design practices.

## Instructions
- MUST implement proper API versioning strategies to maintain backward compatibility. (ID: API_VERSIONING)
- MUST use standard HTTP status codes and error response formats. (ID: HTTP_STANDARDS)
- MUST implement rate limiting and throttling for public APIs. (ID: RATE_LIMITING)

## Priority
High

## Error Handling
- If versioning cannot be implemented, document API changes and maintain compatibility
- If rate limiting is not available, implement basic request validation and document the limitation
