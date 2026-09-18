# Lambda Development

## Purpose
This rule ensures Lambda functions are developed with proper architecture compatibility and local testing.

## Instructions
- MUST test Lambda functions locally using arm64 architecture to ensure compatibility with AWS Lambda's arm64 runtime environment. (ID: LAMBDA_ARM64_TESTING)
- MUST ensure Docker images used for Lambda runtime support arm64 architecture and specify "arm64" Lambda architecture in deployment configurations. (ID: DOCKER_ARM64_SUPPORT)

## Priority
Medium

## Error Handling
- If arm64 testing is not available locally, document the limitation and test on compatible environment
- If Docker image doesn't support arm64, use x86_64 and document the architecture constraint