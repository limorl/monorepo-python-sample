module "appconfig_deployment_strategy_eu_west_1" {
  source = "../../modules/appconfig"
  providers = {
    aws = aws.primary
  }
}

module "appconfig_deployment_strategy_eu_west_2" {
  source = "../../modules/appconfig"
  providers = {
    aws = aws.secondary
  }
}

module "services_eu_west_1" {
  source    = "../../modules/services"
  providers = { aws = aws.primary }
}

module "services_eu_west_2" {
  source    = "../../modules/services"
  providers = { aws = aws.secondary }
}