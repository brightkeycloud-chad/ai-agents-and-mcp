# Demo 2: Evaluating AI Agent Solutions (30 minutes)

## Objective
Show Claude Code and Amazon Q Developer CLI in action across different development and DevOps scenarios, demonstrating when to use each tool.

## Duration
30 minutes total
- Part A: Claude Code (15 min)
- Part B: Amazon Q CLI (15 min)

## Setup Required
- Claude Code CLI installed
- Amazon Q Developer CLI installed
- Legacy app code with issues
- Instruction files configured
- Empty directories for infrastructure generation

## Directory Structure
```
03_use_solutions/
├── README.md                    # This file
├── SECURITY-COMPARISON.md       # Detailed security analysis comparison
├── legacy-app-vulnerable/       # Original app with security vulnerabilities
│   ├── app.py                   # Flask application with security issues
│   ├── models.py                # Database models (vulnerable)
│   ├── utils.py                 # Utility functions (insecure)
│   └── README.md                # Documentation of vulnerabilities
└── legacy-app-secure/           # Secured version of the application
    ├── app.py                   # Hardened Flask application
    ├── models.py                # Secure database models
    ├── utils.py                 # Secure utility functions
    ├── requirements.txt         # Python dependencies
    ├── .env.example             # Environment configuration template
    └── README.md                # Security improvements documentation
```

## Key Demonstrations

### Part A: Claude Code for Development
1. REST API endpoint generation with validation
2. Security vulnerability analysis
3. Legacy code refactoring to modern patterns

### Part B: Amazon Q for DevOps
1. Complete Terraform infrastructure generation
2. Deployment automation script creation
3. CI/CD pipeline troubleshooting and fixes

## Materials Needed
- Terminal windows for both agents
- Code editor to show outputs
- Legacy app prepared with intentional issues
- Broken GitHub Actions workflow file
