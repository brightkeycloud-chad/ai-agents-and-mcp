# DNS Reliability Demo - Terraform Infrastructure

This Terraform configuration creates the infrastructure needed for the DNS reliability demonstration using Amazon Route 53. It deploys web servers in two AWS regions to demonstrate failover capabilities.

## Architecture Overview

The infrastructure includes:
- **Primary Web Server**: EC2 instance in `us-east-2` (Ohio)
- **Secondary Web Server**: EC2 instance in `us-west-2` (Oregon)
- **IAM Role & Instance Profile**: For SSM Session Manager access
- **Security Groups**: Allow HTTP/HTTPS traffic
- **Web Content**: Custom HTML pages identifying each server's role

## Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Terraform installed** (version >= 1.0)
3. **AWS permissions** for:
   - EC2 (instances, security groups, VPCs)
   - IAM (roles, policies, instance profiles)
   - SSM (Session Manager)

## Quick Start

### 1. Initialize Terraform
```bash
cd terraform
terraform init
```

### 2. Review the Plan
```bash
terraform plan
```

### 3. Deploy Infrastructure
```bash
terraform apply
```

Type `yes` when prompted to confirm the deployment.

### 4. Get Output Information
```bash
terraform output
```

## Infrastructure Details

### EC2 Instances
- **Instance Type**: `t4g.micro` (ARM64 architecture)
- **AMI**: Latest Amazon Linux 2023 (ARM64)
- **Networking**: Default VPC, first available subnet
- **Access**: SSM Session Manager (no SSH keys required)

### Web Server Configuration
Each instance runs Apache HTTP server with:
- **Primary Server**: Green-themed page indicating "PRIMARY SERVER - ACTIVE"
- **Secondary Server**: Orange-themed page indicating "SECONDARY SERVER - STANDBY"
- **Health Check Endpoint**: `/health` path for Route 53 monitoring

### Security Groups
- **Inbound**: HTTP (80), HTTPS (443) from anywhere
- **Outbound**: All traffic allowed

### IAM Configuration
- **Role**: `EC2-SSM-Role` with SSM managed instance core policy
- **Instance Profile**: `EC2-SSM-Profile` attached to both instances

## Using the Infrastructure

### 1. Test Web Servers
After deployment, test both servers using the output URLs:
```bash
# Get the URLs
terraform output primary_web_url
terraform output secondary_web_url

# Test with curl
curl $(terraform output -raw primary_web_url)
curl $(terraform output -raw secondary_web_url)
```

### 2. Test Health Check Endpoints
```bash
curl $(terraform output -raw primary_health_check_url)
curl $(terraform output -raw secondary_health_check_url)
```

### 3. Connect via SSM Session Manager
```bash
# Connect to primary server
aws ssm start-session --target $(terraform output -raw ssm_connection_info | jq -r '.primary_instance_id') --region us-east-2

# Connect to secondary server
aws ssm start-session --target $(terraform output -raw ssm_connection_info | jq -r '.secondary_instance_id') --region us-west-2
```

### 4. Get IP Addresses for Route 53
Use these IP addresses when configuring Route 53 health checks:
```bash
terraform output route53_health_check_ips
```

## Route 53 Configuration

After the infrastructure is deployed, use the IP addresses from the output to configure Route 53:

1. **Primary Health Check**: Use the `primary_ip` from output
2. **Secondary Health Check**: Use the `secondary_ip` from output
3. **DNS Records**: Create failover records pointing to these IPs

Follow the main [README.md](../README.md) for detailed Route 53 configuration steps.

## Customization

### Variables
You can customize the deployment by modifying variables:

```bash
# Custom instance type
terraform apply -var="instance_type=t4g.small"

# Custom regions
terraform apply -var="primary_region=us-east-1" -var="secondary_region=eu-west-1"

# Custom tags
terraform apply -var='common_tags={"Environment"="Production","Owner"="TeamName"}'
```

### Variable File
Create a `terraform.tfvars` file for persistent customization:
```hcl
primary_region   = "us-east-1"
secondary_region = "eu-west-1"
instance_type    = "t4g.small"

common_tags = {
  Environment = "Production"
  Owner       = "TeamName"
  CostCenter  = "12345"
}
```

## Monitoring and Troubleshooting

### Check Instance Status
```bash
# Primary instance
aws ec2 describe-instances --instance-ids $(terraform output -raw primary_server_info | jq -r '.instance_id') --region us-east-2

# Secondary instance
aws ec2 describe-instances --instance-ids $(terraform output -raw secondary_server_info | jq -r '.instance_id') --region us-west-2
```

### View Instance Logs
```bash
# Connect via SSM and check Apache logs
sudo tail -f /var/log/httpd/access_log
sudo tail -f /var/log/httpd/error_log
```

### Test Connectivity
```bash
# Test from different locations
curl -I $(terraform output -raw primary_web_url)
curl -I $(terraform output -raw secondary_web_url)
```

## Cost Considerations

This infrastructure uses:
- 2x `t4g.micro` instances (eligible for free tier)
- Standard EBS storage
- Data transfer charges apply
- SSM Session Manager (no additional cost)

Estimated monthly cost: ~$0-20 depending on usage and free tier eligibility.

## Cleanup

To destroy the infrastructure:
```bash
terraform destroy
```

Type `yes` when prompted to confirm the destruction.

## Troubleshooting

### Common Issues

1. **Instances not accessible**
   - Check security group rules
   - Verify instances are in running state
   - Ensure SSM agent is running

2. **Web server not responding**
   - Wait 2-3 minutes for user data script to complete
   - Check instance system logs
   - Verify Apache service status via SSM

3. **SSM connection fails**
   - Ensure IAM role is properly attached
   - Check VPC endpoints for SSM (if using private subnets)
   - Verify AWS CLI configuration

4. **Health checks failing**
   - Confirm security groups allow traffic on port 80
   - Test health check endpoints manually
   - Check Route 53 health checker IP ranges

### Getting Help

1. Check Terraform state: `terraform show`
2. View detailed outputs: `terraform output -json`
3. Check AWS CloudTrail for API calls
4. Review instance system logs in EC2 console

## Security Notes

- Instances use SSM Session Manager (no SSH keys)
- Security groups restrict access to HTTP/HTTPS only
- IAM roles follow least privilege principle
- No hardcoded credentials in configuration

## Next Steps

1. Deploy this infrastructure
2. Test both web servers
3. Follow the main demonstration guide for Route 53 configuration
4. Practice failover scenarios
5. Clean up resources when done

---

This infrastructure provides a solid foundation for demonstrating DNS reliability concepts with Amazon Route 53.
