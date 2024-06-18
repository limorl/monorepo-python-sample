terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # TODO (@limorl): Add state locking using DynamoDB
    bucket = "terraform-backend-450y5"
    key    = "dev/terraform.tfstate"
    region = "us-east-1"    # Primary Region (dev)
  }
}