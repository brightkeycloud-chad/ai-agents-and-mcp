# AI Agents and MCP Training Repository

A comprehensive training repository demonstrating the configuration, usage, and comparison of AI development agents (Claude Code and Kiro) with Model Context Protocol (MCP) server integration. This repository serves as both a learning resource and a practical reference for implementing AI-assisted development workflows with security-first practices.

## Overview

This repository provides hands-on training materials for working with AI development agents, specifically Claude Code and Kiro, integrated with Model Context Protocol (MCP) servers. It demonstrates how to configure, customize, and leverage these agents for secure, efficient software development across multiple domains including application development, infrastructure as code, and DevOps automation.

**Technology Stack:**
- **Languages**: Python 3.8+, Terraform (HCL), Markdown, JSON
- **Frameworks**: Flask 3.0.0 for web applications
- **Security**: Argon2-cffi for password hashing, Bandit for security scanning
- **Testing**: Pytest with coverage reporting
- **Code Quality**: Pylint, Black, MyPy
- **Cloud**: AWS (S3, Lambda) with boto3 SDK
- **AI Agents**: Claude Code CLI, Kiro CLI
- **MCP Servers**: AWS Diagram, AWS Pricing, Terraform, Documentation Generation

## Features

- **Structured Rule Systems**: Comprehensive, priority-based development rules for both Claude Code and Kiro with unique identifiers for tracking and compliance
- **MCP Server Integration**: Practical examples demonstrating diagram generation, cost analysis, pricing estimation, and automated documentation workflows
- **Security-First Development**: Guidelines and real-world examples for secure coding practices including input validation, secure password hashing, and least-privilege access control
- **Legacy Application Hardening**: Before/after demonstrations of securing vulnerable Flask applications with detailed security comparison analysis
- **Infrastructure as Code**: Terraform best practices with multi-file coordination, linting (tflint), and security scanning (checkov)
- **AI Agent Comparison**: Side-by-side evaluation framework showing when to use Claude Code vs Kiro for different tasks
- **Cost Analysis Tools**: AWS architecture visualization with cost estimation and monthly bill analysis examples
- **Automated Documentation**: Workflows for generating comprehensive project documentation using MCP servers

## Prerequisites

### Required AWS Setup
- AWS CLI configured with appropriate credentials (`aws configure`)
- IAM permissions for S3, Lambda, and other services used in examples
- AWS account with billing alerts configured (recommended for cost management examples)
- Optional: AWS Organizations access for multi-account demonstrations

### Development Environment
- **Python**: Version 3.8 or higher with virtual environment support
- **AI Agent CLIs**: 
  - Claude Code CLI installed and configured
  - Kiro CLI installed and configured
- **Version Control**: Git for repository management
- **Editor**: Text editor or IDE with Markdown support (VS Code recommended)
- **Optional Tools**:
  - Terraform CLI for infrastructure examples
  - Docker for containerized demonstrations
  - Node.js for full-stack examples

## Project Components

### Configuration Systems

#### Claude Code Configuration (`01_claude_code_config/`)
Structured instruction files that define how Claude Code should approach development tasks:

- **CLAUDE_big.md**: Comprehensive development guidelines covering code quality, security, testing, and documentation
- **terraform-CLAUDE.md**: Specialized instructions for Terraform development emphasizing multi-file awareness, linting with tflint, and security scanning with checkov

**Key Features:**
- Multi-file coordination strategies
- Security-first development practices
- Terraform-specific best practices
- Change management workflows

#### Kiro Configuration (`02_kiro_config/`)
Priority-based steering system organized by domain for systematic application:

**Steering Categories** (`steering/` directory):
- **Security** (`security/`): Access control (least privilege), data management (encryption, validation), compliance requirements
- **Development** (`development/`): Python virtual environments, error handling, logging, performance optimization, deployment testing, Lambda development
- **Infrastructure** (`IaC/`): Terraform best practices, cost estimation, provider version management
- **General** (`general/`): MCP consultation requirements, planning workflows, error troubleshooting
- **API** (`api/`): Design standards, versioning, rate limiting
- **Monitoring** (`monitoring/`): Observability, KPI tracking, alerting
- **Compliance** (`compliance/`): Audit logging, resource tagging, security reviews
- **Resilience** (`resilience/`): Disaster recovery, backup strategies, multi-AZ design
- **Documentation** (`documentation/`): Code documentation generation using MCP servers

**Implementation Phases:**
1. **Phase 1 - Critical Rules** (6 rules): Security fundamentals, MCP consultation, planning
2. **Phase 2 - High Priority** (8 rules): Development standards, IaC practices, error handling
3. **Phase 3 - Medium Priority** (4 rules): Performance optimization, cost estimation, monitoring

### Demonstration Examples

#### Use Solutions (`03_use_solutions/`)
Practical demonstrations of AI agents solving real-world problems:

- **legacy-app-vulnerable/**: Original Flask application with intentional security vulnerabilities (weak password hashing, SQL injection risks, insecure file handling)
- **legacy-app-secure/**: Hardened version demonstrating security best practices:
  - Argon2 password hashing with proper salt and iteration counts
  - Input validation and sanitization
  - AWS S3 integration with temporary credentials (STS)
  - Comprehensive test suite (pytest)
  - Security scanning (Bandit)
  - Code quality enforcement (Black, Pylint, MyPy)
- **SECURITY-COMPARISON.md**: Detailed analysis comparing vulnerable vs secure implementations

#### MCP Tests (`04_mcp_tests/`)
Hands-on examples demonstrating MCP server capabilities:

**01_diagrams/**: AWS architecture diagram generation
- `diagram_only/`: Basic diagram generation workflow
- `knowledge_and_diagram/`: Combining AWS knowledge base with diagram generation
- Demonstrates using AWS official icon sets for professional visualizations

**02_cost_analysis/**: Cost estimation and analysis workflows
- `01_diagram_cost/`: Analyzing architecture diagrams for cost implications
- `02_monthly_bill_analysis/`: AWS bill analysis and optimization recommendations
- Integration with AWS Pricing API for accurate estimates

**03_simple_app/**: Complete application generation workflow
- Stable Diffusion image generation web application
- GPU utilization for model inference
- Front-end best practices using MCP guidance
- Programmatic testing at each development step

### Development Projects

#### Agents MCP Development (`07_agents_mcp_development/`)
Advanced examples of custom agent development:
- **MTG_CARD_CREATOR_PROMPT.md**: Specialized prompt for Magic: The Gathering card generation
- Custom Claude Code skills for domain-specific tasks
- Demonstrates extending agent capabilities for niche use cases

#### Agents MCP DevOps (`08_agents_mcp_devops/`)
DevOps automation with AI agents:

**01_terraform_agent/**: Cloud engineering agent specialized in Terraform
- **terraform-cloud-engineer-agent.json**: Agent configuration with specialized tools and prompt
- **terraform/**: Complete Terraform module example with:
  - Multi-file organization (main.tf, variables.tf, outputs.tf)
  - State management configuration
  - Example infrastructure deployment
  - Cost estimation integration

## Getting Started

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd ai-agents-and-mcp

# Verify Python version
python3 --version  # Should be 3.8 or higher
```

### 2. Configure AI Agents

**For Kiro:**
```bash
# Steering files are automatically loaded from ~/.kiro/steering/
# Copy example steering files to your configuration directory
cp -r 02_kiro_config/steering/* ~/.kiro/steering/

# Verify steering files are loaded
ls ~/.kiro/steering/
```

**For Claude Code:**
```bash
# Review configuration files
cat 01_claude_code_config/CLAUDE_big.md
cat 01_claude_code_config/terraform-CLAUDE.md

# Configure Claude Code to use these instruction files
# (Refer to Claude Code CLI documentation for configuration)
```

### 3. Set Up Python Environment (for Flask examples)

```bash
cd 03_use_solutions/legacy-app-secure

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure AWS (for cloud examples)

```bash
# Configure AWS CLI
aws configure
# Enter your AWS Access Key ID, Secret Access Key, region, and output format

# Verify configuration
aws sts get-caller-identity

# Optional: Set up AWS profile for testing
aws configure --profile training
```

## Usage Examples

### Using the Rule Systems

**Kiro with Steering:**
```bash
# Steering files are automatically applied from ~/.kiro/steering/
# Start a conversation and steering will be consulted

# Example: Ask Kiro to create a Lambda function
# Kiro will automatically apply steering for:
# - Python virtual environment (PYTHON_VENV_REQUIRED)
# - Error handling (ERROR_HANDLING)
# - Least privilege IAM (LEAST_PRIVILEGE)
# - Testing requirements (TESTING)
```

**Claude Code with Instructions:**
```bash
# Reference instruction files in your prompts
# Example: "Follow the guidelines in 01_claude_code_config/terraform-CLAUDE.md 
# to create a Terraform module for an S3 bucket"
```

### Running the Secure Application

```bash
cd 03_use_solutions/legacy-app-secure

# Activate virtual environment
source venv/bin/activate

# Set up environment variables
cp .env.example .env
# Edit .env with your AWS credentials and configuration

# Run the application
python app.py

# Application will be available at http://localhost:5000
```

### Security Scanning

```bash
cd 03_use_solutions/legacy-app-secure

# Run comprehensive security analysis
bandit -r . -f json -o security-report.json

# Run code quality checks
pylint *.py
black --check *.py
mypy *.py

# Run tests with coverage
pytest --cov=. --cov-report=html
```

### MCP Server Examples

**Generate AWS Architecture Diagram:**
```bash
cd 04_mcp_tests/01_diagrams/diagram_only

# Review the prompt
cat prompt.txt

# Use with your AI agent to generate diagram
# The agent will use the AWS Diagram MCP server to create visualizations
```

**Cost Analysis:**
```bash
cd 04_mcp_tests/02_cost_analysis/01_diagram_cost

# Analyze architecture for cost implications
# Review the generated cost analysis
cat aws_architecture_cost_analysis.md
```

### Terraform Development

```bash
cd 08_agents_mcp_devops/01_terraform_agent/terraform

# Initialize Terraform
terraform init

# Format code
terraform fmt

# Validate configuration
terraform validate

# Plan deployment
terraform plan

# Apply (with approval)
terraform apply
```

## Architecture

The repository follows a modular structure designed for progressive learning and practical application:

```
ai-agents-and-mcp/
├── 01_claude_code_config/          # Claude Code instruction files
│   ├── CLAUDE_big.md               # Comprehensive development guidelines
│   └── terraform-CLAUDE.md         # Terraform-specific instructions
│
├── 02_kiro_config/                 # Kiro steering system
│   └── steering/                   # Organized by domain
│       ├── security/               # Access control, data management
│       ├── development/            # Python, error handling, testing
│       ├── IaC/                    # Terraform, cost estimation
│       ├── general/                # MCP consultation, planning
│       ├── api/                    # API design standards
│       ├── monitoring/             # Observability, alerting
│       ├── compliance/             # Governance, audit logging
│       ├── resilience/             # Disaster recovery, backups
│       ├── documentation/          # Code documentation
│       └── conversation.rule.md    # Conversation behavior rules
│
├── 03_use_solutions/               # Practical demonstrations
│   ├── legacy-app-vulnerable/      # Insecure Flask app (before)
│   ├── legacy-app-secure/          # Secured Flask app (after)
│   └── SECURITY-COMPARISON.md      # Security analysis
│
├── 04_mcp_tests/                   # MCP server demonstrations
│   ├── 01_diagrams/                # AWS diagram generation
│   ├── 02_cost_analysis/           # Cost estimation workflows
│   └── 03_simple_app/              # Complete app generation
│
├── 07_agents_mcp_development/      # Custom agent development
│   └── .claude/skills/             # Custom Claude Code skills
│
├── 08_agents_mcp_devops/           # DevOps automation
│   └── 01_terraform_agent/         # Terraform specialist agent
│       ├── terraform/              # Example infrastructure
│       └── terraform-cloud-engineer-agent.json
│
├── generated-docs/                 # Auto-generated documentation
└── .claude/                        # Claude Code settings
```

### Design Principles

1. **Progressive Complexity**: Examples start simple and build to advanced use cases
2. **Security First**: All examples emphasize secure coding practices
3. **Practical Application**: Real-world scenarios with production-ready code
4. **Tool Integration**: Demonstrates MCP server capabilities throughout
5. **Comparison Framework**: Shows when to use each AI agent for specific tasks

## Next Steps

### Enhancements

**Custom MCP Servers:**
- Develop organization-specific MCP servers for proprietary systems
- Create domain-specific knowledge bases for specialized industries
- Integrate with internal APIs and documentation systems

**CI/CD Integration:**
- Implement rule systems in GitHub Actions workflows
- Automate security scanning in pull request checks
- Generate cost estimates for infrastructure changes automatically
- Create deployment pipelines using agent-generated configurations

**Team Adoption:**
- Customize rules for your team's technology stack and standards
- Create team-specific instruction files for common tasks
- Establish governance policies for AI agent usage
- Train team members on effective prompt engineering

**Security Automation:**
- Integrate Bandit security scanning into pre-commit hooks
- Automate dependency vulnerability scanning with Safety
- Implement automated secret detection
- Create security dashboards for continuous monitoring

### Contributing

We welcome contributions that enhance the training materials or add new examples:

1. **Fork the repository** and create a feature branch
2. **Follow established patterns**: Use the rule systems in your development
3. **Add comprehensive tests**: All new code should include test coverage
4. **Document your changes**: Update relevant README files and add inline comments
5. **Security review**: Ensure all examples follow security best practices
6. **Submit a pull request** with:
   - Clear description of changes
   - Rationale for the enhancement
   - Testing evidence
   - Documentation updates

**Contribution Ideas:**
- Additional MCP server integration examples
- New security hardening demonstrations
- Multi-cloud examples (Azure, GCP)
- Advanced Terraform patterns
- CI/CD pipeline templates
- Custom agent configurations for specific domains

## Clean Up

### Development Environment

```bash
# Deactivate Python virtual environment
deactivate

# Remove virtual environment (if needed)
rm -rf venv

# Clean up Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### AWS Resources

If you've deployed AWS resources during testing, clean them up to avoid charges:

```bash
# List and delete S3 buckets created during testing
aws s3 ls
aws s3 rb s3://your-test-bucket-name --force

# List and delete Lambda functions
aws lambda list-functions
aws lambda delete-function --function-name your-test-function

# Check for other resources
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table
aws rds describe-db-instances --query 'DBInstances[*].[DBInstanceIdentifier,DBInstanceStatus]' --output table

# Terraform cleanup (if you deployed infrastructure)
cd 08_agents_mcp_devops/01_terraform_agent/terraform
terraform destroy
```

### Generated Files

```bash
# Remove generated documentation
rm -rf generated-docs/

# Remove generated diagrams
find . -type d -name "generated-diagrams" -exec rm -rf {} +

# Remove test reports
rm -rf htmlcov/
rm -f .coverage
rm -f security-report.json
```

## Troubleshooting

### Common Issues

#### Virtual Environment Issues

**Problem**: `python3: command not found` or version mismatch

**Solution**:
```bash
# Check Python installation
which python3
python3 --version

# On macOS, install via Homebrew
brew install python@3.11

# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv

# Verify PATH configuration
echo $PATH
```

**Problem**: Virtual environment activation fails

**Solution**:
```bash
# Ensure venv module is available
python3 -m venv --help

# Try alternative activation methods
source venv/bin/activate  # bash/zsh
. venv/bin/activate       # sh
venv\Scripts\activate.bat # Windows cmd
venv\Scripts\Activate.ps1 # Windows PowerShell
```

#### MCP Server Connection Issues

**Problem**: MCP server not responding or connection timeout

**Solution**:
```bash
# Verify MCP server installation
# Check configuration files in ~/.kiro/ or Claude Code settings

# Test network connectivity
ping api.anthropic.com

# Check firewall settings
# Ensure ports are not blocked by corporate firewall

# Review MCP server logs
# Location varies by MCP server implementation
```

**Problem**: MCP server returns errors or unexpected results

**Solution**:
- Verify API credentials are correctly configured
- Check rate limits and quota usage
- Review MCP server documentation for version compatibility
- Update MCP server to latest version

#### Security Scanning False Positives

**Problem**: Bandit reports issues in safe code

**Solution**:
```bash
# Create or update .bandit configuration
cat > .bandit << EOF
[bandit]
exclude_dirs = /test,/venv
skips = B101,B601
EOF

# Add inline comments to suppress specific warnings
# Example: # nosec B603

# Review and update Bandit to latest version
pip install --upgrade bandit
```

#### AWS Credential Issues

**Problem**: `Unable to locate credentials` or `Access Denied` errors

**Solution**:
```bash
# Verify AWS CLI configuration
aws configure list
aws sts get-caller-identity

# Check credentials file
cat ~/.aws/credentials

# Verify IAM permissions
aws iam get-user
aws iam list-attached-user-policies --user-name YOUR_USERNAME

# Test with specific profile
aws s3 ls --profile training

# Refresh temporary credentials if using STS
aws sts get-session-token --duration-seconds 3600
```

#### Terraform Issues

**Problem**: `terraform init` fails or provider download errors

**Solution**:
```bash
# Clear Terraform cache
rm -rf .terraform/
rm .terraform.lock.hcl

# Re-initialize with upgrade flag
terraform init -upgrade

# Use specific provider version
terraform init -upgrade=true

# Check network connectivity to registry
curl https://registry.terraform.io/v1/providers/hashicorp/aws
```

**Problem**: State lock errors

**Solution**:
```bash
# Force unlock (use with caution)
terraform force-unlock LOCK_ID

# Verify state backend configuration
terraform state list

# Check for concurrent operations
ps aux | grep terraform
```

### Getting Help

**Documentation Resources:**
- Review steering documentation in `02_kiro_config/steering/README.md`
- Check secure application example in `03_use_solutions/legacy-app-secure/README.md`
- Consult security comparison in `03_use_solutions/SECURITY-COMPARISON.md`
- Reference MCP server documentation for integration issues

**Community Support:**
- Open an issue in the repository with detailed error information
- Include relevant log files and configuration (redact sensitive information)
- Provide steps to reproduce the issue
- Specify your environment (OS, Python version, AI agent version)

**Debugging Tips:**
- Enable verbose logging in AI agent configurations
- Use `set -x` in bash scripts for detailed execution traces
- Check system logs for underlying issues
- Test components in isolation to identify the problem area

## License

This project is provided as training material for educational purposes. Users should review and comply with their organization's policies regarding:
- AI agent usage and data privacy
- Cloud resource provisioning and cost management
- Security practices and compliance requirements
- Open source software licensing

When using this repository in production environments, ensure all security practices are reviewed and approved by your organization's security team. The examples provided are for demonstration purposes and should be adapted to meet your specific security and compliance requirements.