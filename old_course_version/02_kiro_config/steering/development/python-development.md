# Python Development

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
