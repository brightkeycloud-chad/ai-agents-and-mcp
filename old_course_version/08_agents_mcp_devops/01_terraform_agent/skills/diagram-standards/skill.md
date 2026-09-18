---
name: Architecture Diagram Standards
description: Standards for generating architecture diagrams using AWS Diagram MCP
inclusion: manual
---

# Architecture Diagram Standards

Use AWS Diagram MCP for creating architecture diagrams (supports AWS, K8s, on-prem, and custom diagrams).

## Workflow

**New diagrams:**
- Generate diagram using AWS Diagram MCP
- Save the diagram generation code alongside infrastructure files
- Enables future updates to modify existing diagram (preserves layout)

**Updating existing diagrams:**
- Locate the saved diagram generation code
- Update code to reflect infrastructure changes
- Regenerate diagram from updated code (maintains consistent layout)

## Diagram Standards

- Show ALL infrastructure resources and their associations
- Display resource relationships clearly with arrows/connections
- Use appropriate AWS service icons
- Group related resources with Clusters
- Label resources with meaningful names

## Terraform-Specific Rules

When diagramming Terraform infrastructure:

- Include ALL resources defined in `.tf` files
- Show data sources as their actual resource type (not labeled as "data")
  - Example: `data "aws_vpc"` → display as VPC resource
- Reflect resource dependencies and associations from Terraform code
- Match resource names from Terraform definitions

## File Organization

Save diagram code as:
- `diagram.py` or `<project>-diagram.py` in project root
- Or in `docs/diagrams/` directory for larger projects
