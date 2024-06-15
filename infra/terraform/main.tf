terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # TODO (@limorl): Add state locking using DynamoDB
    # Backend configuration in backend.*.tfvars file
  }
}

provider "aws" {
  region = var.aws_primary_region

  default_tags {
    tags = {
      Environment = var.stage
      Region      = var.aws_region
      Deployment  = "terraform-github-workflow"
    }
  }
}