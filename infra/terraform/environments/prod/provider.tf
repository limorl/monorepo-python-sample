provider "aws" {
  alias  = "prod-primary"
  region = var.aws_primary_region

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}

provider "aws" {
  alias  = "prod-secondary"
  region = var.aws_secondary_region

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}