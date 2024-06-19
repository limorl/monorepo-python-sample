module "appconfig_deployment_strategy_eu_west_1" {
  source = "../../modules/appconfig"
  providers = {
    aws = aws.staging-primary
  }
}

module "appconfig_deployment_strategy_eu_west_2" {
  source = "../../modules/appconfig"
  providers = {
    aws = aws.staging-secondary
  }
}

module "services_eu_west_1" {
  source    = "../../modules/services"
  providers = { aws = aws.staging-primary }
}

module "services_eu_west_2" {
  source    = "../../modules/services"
  providers = { aws = aws.staging-secondary }
}