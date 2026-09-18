# Output values for the DNS reliability demonstration

output "primary_server_info" {
  description = "Information about the primary web server"
  value = {
    instance_id       = aws_instance.primary_web_server.id
    public_ip         = aws_instance.primary_web_server.public_ip
    private_ip        = aws_instance.primary_web_server.private_ip
    public_dns        = aws_instance.primary_web_server.public_dns
    region            = var.primary_region
    availability_zone = aws_instance.primary_web_server.availability_zone
    instance_type     = aws_instance.primary_web_server.instance_type
    ami_id            = aws_instance.primary_web_server.ami
  }
}

output "secondary_server_info" {
  description = "Information about the secondary web server"
  value = {
    instance_id       = aws_instance.secondary_web_server.id
    public_ip         = aws_instance.secondary_web_server.public_ip
    private_ip        = aws_instance.secondary_web_server.private_ip
    public_dns        = aws_instance.secondary_web_server.public_dns
    region            = var.secondary_region
    availability_zone = aws_instance.secondary_web_server.availability_zone
    instance_type     = aws_instance.secondary_web_server.instance_type
    ami_id            = aws_instance.secondary_web_server.ami
  }
}

output "primary_web_url" {
  description = "URL to access the primary web server"
  value       = "http://${aws_instance.primary_web_server.public_ip}"
}

output "secondary_web_url" {
  description = "URL to access the secondary web server"
  value       = "http://${aws_instance.secondary_web_server.public_ip}"
}

output "primary_health_check_url" {
  description = "Health check endpoint for the primary server"
  value       = "http://${aws_instance.primary_web_server.public_ip}${var.health_check_path}"
}

output "secondary_health_check_url" {
  description = "Health check endpoint for the secondary server"
  value       = "http://${aws_instance.secondary_web_server.public_ip}${var.health_check_path}"
}

output "route53_health_check_ips" {
  description = "IP addresses to use for Route 53 health checks"
  value = {
    primary_ip   = aws_instance.primary_web_server.public_ip
    secondary_ip = aws_instance.secondary_web_server.public_ip
  }
}

output "ssm_connection_info" {
  description = "Information for connecting via SSM Session Manager"
  value = {
    primary_instance_id       = aws_instance.primary_web_server.id
    secondary_instance_id     = aws_instance.secondary_web_server.id
    connect_command_primary   = "aws ssm start-session --target ${aws_instance.primary_web_server.id} --region ${var.primary_region}"
    connect_command_secondary = "aws ssm start-session --target ${aws_instance.secondary_web_server.id} --region ${var.secondary_region}"
  }
}

output "security_groups" {
  description = "Security group information"
  value = {
    primary_sg_id   = aws_security_group.web_sg_primary.id
    secondary_sg_id = aws_security_group.web_sg_secondary.id
  }
}

output "iam_role_info" {
  description = "IAM role and instance profile information"
  value = {
    role_name             = aws_iam_role.ec2_ssm_role.name
    role_arn              = aws_iam_role.ec2_ssm_role.arn
    instance_profile_name = aws_iam_instance_profile.ec2_ssm_profile.name
    instance_profile_arn  = aws_iam_instance_profile.ec2_ssm_profile.arn
  }
}

output "demonstration_summary" {
  description = "Summary information for the DNS reliability demonstration"
  value = {
    primary_server = {
      region     = "${var.primary_region}"
      role       = "Primary"
      url        = "http://${aws_instance.primary_web_server.public_ip}"
      health_url = "http://${aws_instance.primary_web_server.public_ip}${var.health_check_path}"
      ip_address = aws_instance.primary_web_server.public_ip
    }
    secondary_server = {
      region     = "${var.secondary_region}"
      role       = "Secondary"
      url        = "http://${aws_instance.secondary_web_server.public_ip}"
      health_url = "http://${aws_instance.secondary_web_server.public_ip}${var.health_check_path}"
      ip_address = aws_instance.secondary_web_server.public_ip
    }
    next_steps = [
      "1. Wait 2-3 minutes for instances to fully initialize",
      "2. Test both web servers using the URLs above",
      "3. Use the IP addresses for Route 53 health checks",
      "4. Follow the README.md instructions for Route 53 configuration"
    ]
  }
}
