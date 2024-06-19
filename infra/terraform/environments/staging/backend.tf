terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  backend "s3" {
    # TODO (@limorl): Add state locking using DynamoDB
    bucket = "terraform-backend-staging-450y5"
    key    = "staging/terraform.tfstate"
    region = "eu-west-1" # Primary Region (staging)
    dynamodb_table = "terraform-state-lock"
  }
}