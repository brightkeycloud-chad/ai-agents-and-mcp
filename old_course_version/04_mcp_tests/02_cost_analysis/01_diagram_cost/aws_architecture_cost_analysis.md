# AWS Three-Tier Architecture Cost Analysis

## Architecture Overview

Based on the diagram analysis, this is a comprehensive three-tier web application architecture deployed across multiple AWS Availability Zones with the following components:

### **Presentation Tier (Public Subnets)**
- Internet Gateway for external access
- NAT Gateways (2x) for outbound internet access from private subnets
- Application Load Balancer (ALB) for traffic distribution

### **Application Tier (Private Subnets)**
- ECS Fargate cluster with 3 tasks/services
- Auto Scaling Group for dynamic scaling
- AWS WAF for web application firewall protection
- SSL Certificate Manager (ACM) for HTTPS termination

### **Data Tier (Private Subnets)**
- RDS PostgreSQL Multi-AZ deployment (Primary + Standby)
- Read Replicas (2x) for read scaling
- AWS Secrets Manager for database credentials

### **Supporting Services**
- Amazon ECR for container image storage
- IAM Roles & Policies for security
- CloudWatch for monitoring and logging

---

## Persistent Monthly Costs (Always Running)

### **Compute Services**
| Service | Configuration | Monthly Cost (USD) |
|---------|--------------|-------------------|
| **ECS Fargate Tasks** | 3 tasks × 0.5 vCPU, 1GB RAM × 24/7 | ~$32.40 |
| **Application Load Balancer** | 1 ALB with basic usage | ~$16.20 |
| **NAT Gateways** | 2 NAT Gateways × 24/7 | ~$90.00 |

### **Database Services**
| Service | Configuration | Monthly Cost (USD) |
|---------|--------------|-------------------|
| **RDS PostgreSQL Multi-AZ** | db.t3.micro Primary + Standby | ~$25.00 |
| **RDS Read Replicas** | 2 × db.t3.micro replicas | ~$25.00 |
| **RDS Storage** | 20GB GP2 × 4 instances | ~$8.00 |

### **Security & Management**
| Service | Configuration | Monthly Cost (USD) |
|---------|--------------|-------------------|
| **AWS Secrets Manager** | 1 secret for DB credentials | ~$0.40 |
| **AWS WAF** | Basic web ACL with rules | ~$5.00 |
| **Internet Gateway** | No charge for gateway itself | $0.00 |

### **Container Registry**
| Service | Configuration | Monthly Cost (USD) |
|---------|--------------|-------------------|
| **Amazon ECR** | 3 repositories, ~2GB storage | ~$0.20 |

**Total Persistent Monthly Costs: ~$202.20**

---

## Variable Costs (Development Usage Estimates)

### **Data Transfer**
| Type | Development Usage | Monthly Cost (USD) |
|------|------------------|-------------------|
| **Internet Outbound** | 10GB/month | ~$0.90 |
| **NAT Gateway Processing** | 5GB/month | ~$0.23 |
| **ALB Data Processing** | 20GB/month | ~$1.60 |

### **Monitoring & Logging**
| Service | Development Usage | Monthly Cost (USD) |
|---------|------------------|-------------------|
| **CloudWatch Logs** | 5GB ingestion, 30-day retention | ~$2.50 |
| **CloudWatch Metrics** | Custom metrics for app monitoring | ~$3.00 |
| **CloudWatch Alarms** | 10 alarms for basic monitoring | ~$1.00 |

### **Development Activities**
| Activity | Usage Pattern | Monthly Cost (USD) |
|----------|--------------|-------------------|
| **ECR Data Transfer** | 50 image pulls/month | ~$0.05 |
| **RDS Backup Storage** | 20GB automated backups | ~$2.00 |
| **ECS Task Scaling** | Occasional scale-out events | ~$5.00 |

**Total Variable Monthly Costs: ~$16.28**

---

## Cost Optimization Recommendations

### **Immediate Savings (Development Environment)**
1. **Use Spot Instances**: Replace Fargate with EC2 Spot instances (~70% savings on compute)
2. **Single AZ Deployment**: Remove Multi-AZ for development (~50% RDS savings)
3. **Reduce NAT Gateways**: Use single NAT Gateway (~$45/month savings)
4. **Smaller Instance Types**: Use db.t3.nano for development databases (~60% savings)

### **Estimated Optimized Development Costs**
- **Persistent Costs**: ~$85-100/month (58% reduction)
- **Variable Costs**: ~$16/month (minimal change)
- **Total Optimized**: ~$101-116/month

### **Production Scaling Considerations**
- **Auto Scaling**: Costs will scale with traffic (2-10x during peak usage)
- **Data Transfer**: Can increase significantly with user growth
- **Storage**: Database and log storage will grow over time
- **Reserved Instances**: 30-60% savings for predictable workloads

---

## Cost Monitoring Setup

### **Recommended CloudWatch Alarms**
1. Monthly spend threshold alerts
2. Unusual data transfer spikes
3. ECS task scaling events
4. RDS connection count monitoring

### **Cost Allocation Tags**
- Environment: development/staging/production
- Project: application-name
- Owner: team-name
- Cost-Center: department

---

## Summary

This three-tier architecture provides high availability and scalability but comes with significant persistent costs (~$202/month) primarily driven by:
- NAT Gateways (44% of persistent costs)
- Database Multi-AZ deployment (25% of persistent costs)
- ECS Fargate compute (16% of persistent costs)

For development environments, implementing the optimization recommendations can reduce costs by approximately 50% while maintaining core functionality for testing and development activities.

**Note**: All pricing estimates are based on US East (N. Virginia) region and current AWS pricing as of November 2024. Actual costs may vary based on specific usage patterns, data transfer volumes, and regional pricing differences.
