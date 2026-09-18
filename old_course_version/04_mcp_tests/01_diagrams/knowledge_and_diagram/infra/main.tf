terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.39"
    }
  }

  backend "s3" {
    bucket         = "terraform-state-bucket"
    key            = "three-tier/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      env        = var.env
      costcenter = var.costcenter
      managed-by = "terraform"
      repo       = var.repo
      directory  = "infra"
    }
  }
}

locals {
  name_prefix = "${var.env}-${var.project}"
}

# --- Data Sources ---

data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}
