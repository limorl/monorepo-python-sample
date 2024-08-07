terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-backend-dev-450y5"
    key            = "dev/terraform.tfstate"
    region         = "eu-west-1" # Primary Region (dev)
    dynamodb_table = "tfstate-lock-dev"
  }
}