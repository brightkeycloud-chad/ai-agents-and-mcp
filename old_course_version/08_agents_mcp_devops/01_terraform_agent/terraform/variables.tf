# Variables for DNS Reliability Demonstration Infrastructure

variable "primary_region" {
  description = "Primary AWS region for the demonstration"
  type        = string
  default     = "us-east-2"
  
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.primary_region))
    error_message = "Primary region must be a valid AWS region format (e.g., us-east-2)."
  }
}

variable "secondary_region" {
  description = "Secondary AWS region for the demonstration"
  type        = string
  default     = "us-west-2"
  
  validation {
    condition     = can(regex("^[a-z]{2}-[a-z]+-[0-9]$", var.secondary_region))
    error_message = "Secondary region must be a valid AWS region format (e.g., us-west-2)."
  }
}

variable "instance_type" {
  description = "EC2 instance type for web servers"
  type        = string
  default     = "t4g.micro"
  
  validation {
    condition     = can(regex("^t4g\\.", var.instance_type))
    error_message = "Instance type must be ARM-based (t4g family) for this demonstration."
  }
}

variable "architecture" {
  description = "CPU architecture for the AMI"
  type        = string
  default     = "arm64"
  
  validation {
    condition     = contains(["arm64", "x86_64"], var.architecture)
    error_message = "Architecture must be either 'arm64' or 'x86_64'."
  }
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default = {
    Purpose     = "DNS-Reliability-Demo"
    Environment = "Training"
    Project     = "AWS-Foundations-Video"
    ManagedBy   = "Terraform"
  }
}

variable "enable_detailed_monitoring" {
  description = "Enable detailed CloudWatch monitoring for EC2 instances"
  type        = bool
  default     = false
}

variable "web_server_port" {
  description = "Port for the web server"
  type        = number
  default     = 80
  
  validation {
    condition     = var.web_server_port > 0 && var.web_server_port <= 65535
    error_message = "Web server port must be between 1 and 65535."
  }
}

variable "health_check_path" {
  description = "Path for health check endpoint"
  type        = string
  default     = "/health"
  
  validation {
    condition     = can(regex("^/", var.health_check_path))
    error_message = "Health check path must start with '/'."
  }
}

variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access the web servers"
  type        = list(string)
  default     = ["0.0.0.0/0"]
  
  validation {
    condition = alltrue([
      for cidr in var.allowed_cidr_blocks : can(cidrhost(cidr, 0))
    ])
    error_message = "All CIDR blocks must be valid CIDR notation."
  }
}

variable "iam_role_name" {
  description = "Name for the IAM role used by EC2 instances"
  type        = string
  default     = "EC2-SSM-Role"
  
  validation {
    condition     = can(regex("^[a-zA-Z0-9+=,.@_-]+$", var.iam_role_name))
    error_message = "IAM role name must contain only alphanumeric characters and +=,.@_- characters."
  }
}

variable "instance_profile_name" {
  description = "Name for the IAM instance profile"
  type        = string
  default     = "EC2-SSM-Profile"
  
  validation {
    condition     = can(regex("^[a-zA-Z0-9+=,.@_-]+$", var.instance_profile_name))
    error_message = "Instance profile name must contain only alphanumeric characters and +=,.@_- characters."
  }
}
