provider "aws" {
  alias  = "staging-primary"
  region = "eu-west-1"

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}

provider "aws" {
  alias  = "staging-secondary"
  region = "eu-west-2"

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}