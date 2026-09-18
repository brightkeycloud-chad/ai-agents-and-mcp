# Performance Optimization

## Purpose
This rule ensures performance considerations are integrated into all development decisions.

## Instructions
- MUST consider performance implications for all code changes including database queries, API calls, and resource utilization. (ID: PERFORMANCE_ANALYSIS)
- MUST implement caching strategies where appropriate to reduce redundant operations and improve response times. (ID: CACHING_STRATEGY)
- MUST profile and benchmark critical code paths before and after changes. (ID: PERFORMANCE_BENCHMARKING)

## Priority
High

## Error Handling
- If performance profiling tools are not available, use basic timing measurements and document the limitation
- If caching cannot be implemented, optimize algorithms and document performance constraints
