---
name: Terraform AWS Standards
description: Enforces Terraform coding standards for AWS infrastructure
inclusion: manual
---

# Terraform AWS Standards

You are reviewing Terraform code for AWS infrastructure. Enforce these standards:

## Naming Conventions

- Pattern: `{env}-{service}-{resource}` (keep concise, avoid excessive length)
- Format: kebab-case, all lowercase
- Examples: `prod-api-gateway`, `dev-vpc-main`

## Required Tags

All taggable resources MUST include:

```hcl
tags = {
  env          = "prod|dev|staging"
  costcenter   = "<cost-center-code>"
  managed-by   = "terraform"
  repo         = "<github-repo-name>"
  directory    = "<path-within-repo>"
}
```

## Modules vs Resources

- Use AWS provider modules when replacing 3+ individual resources
- Prefer loops (`for_each`, `count`) for simple resources with:
  - Unlikely need for custom configuration
  - Simple parameters
  - Repetitive patterns

## Variables vs Data Sources

- Data sources: Query existing AWS resources
- Variables: Define new resource parameters

## Documentation Requirements

Code must support automatic documentation generation:

- Use `description` in all variable and output blocks
- Add comments for complex logic
- Structure enables diagram generation (clear resource relationships)
- Group related resources logically

## Services Focus

Primary: Core AWS services and edge networking
Scope: Any AWS service as needed

## Formatting and Validation

- Always run `terraform fmt` for proper formatting
- Verify code with `terraform validate` before committing

## Review Checklist

When reviewing Terraform code, verify:

1. Naming follows conventions
2. All required tags present
3. Opportunities for modules/loops identified
4. Variables vs data sources used appropriately
5. Documentation-ready structure
6. Code formatted with `terraform fmt`
7. Code validated with `terraform validate`
