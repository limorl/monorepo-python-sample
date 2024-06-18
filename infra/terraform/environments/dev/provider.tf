provider "aws" {
  alias  = "primary"
  region = var.aws_primary_region

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}