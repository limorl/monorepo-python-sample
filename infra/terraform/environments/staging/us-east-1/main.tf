
# For now, we're deploying in a single region, which is the primary region
# We are not creating the RDS Postgress and ssm tunnel resources

locals {
  env                = "staging"
  primary_region     = "us-east-1"
  current_region     = "us-east-1"
  global_key         = "450y5"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  #ssm_instance_ami                = "ami-05550e886fd83b2c7"
  #ssm_instance_type               = "t3.micro"
}

module "shared" {
  source = "../../../modules/shared"

  env                = local.env
  primary_region     = local.primary_region
  current_region     = local.current_region
  global_key         = local.global_key
  availability_zones = local.availability_zones
  #ssm_instance_ami                   = local.ssm_instance_ami
  #ssm_instance_type                  = local.ssm_instance_type

  providers = {
    aws = aws
  }
}

# Test resources are deployed only on non-prod environment
module "test_resources" {
  source = "../../../modules/tests"
  env    = local.env
}
