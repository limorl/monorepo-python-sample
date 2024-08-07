terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    bucket         = "terraform-backend-staging-450y5"
    key            = "staging/terraform.tfstate"
    region         = "us-east-1" # Primary Region (staging)
    dynamodb_table = "tfstate-lock-staging"
  }
}