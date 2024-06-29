terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-backend-prod-450y5"
    key            = "prod/terraform.tfstate"
    region         = "us-west-1" # Primary Region (prod)
    dynamodb_table = "terraform-state-lock"
  }
}