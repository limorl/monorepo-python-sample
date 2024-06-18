provider "aws" {
  alias  = "primary"
  region = "us-west-1"

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}

provider "aws" {
  alias  = "secondary"
  region = "us-west-2"

  default_tags {
    tags = {
      Environment = var.stage
      Deployment  = "terraform"
    }
  }
}