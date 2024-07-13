# For now, we're deploying in a single region. To support a secondary region, duplicate the resources,
# replace the siffix -primary with -secondary and use aws.staging-secondary provider

module "services_primary" {
  source = "../../modules/services"
  providers = {
    aws = aws.staging-primary
  }
}

resource "aws_appconfig_deployment_strategy" "deployment_strategy_primary" {
  name                           = "staging-deployment-strategy"
  provider                       = aws.staging-primary
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = {
    Type = "appconfig_deployment_strategy"
  }
}

module "test_resources_primary" {
  source = "../../modules/tests"
  stage  = var.stage

  providers = {
    aws = aws.staging-primary
  }
}
