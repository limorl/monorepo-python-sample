# For now, we're deploying in a single region, which is the primary region
# We are not creating the RDS Postgress and ssm tunnel resources

locals {
  env                = "dev"
  primary_region     = "eu-west-1"
  current_region     = "eu-west-1"
  global_key         = "450y5"
  availability_zones = ["eu-west-1a", "eu-west-1b", "eu-west-1c"]
  #ssm_instance_ami                = "ami-044b38f6920d7a32f"
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
