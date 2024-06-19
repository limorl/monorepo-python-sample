module "appconfig_deployment_strategy_us_west_1" {
  source = "../../modules/appconfig"
  providers = {
    aws = aws.prod-primary
  }
}

module "appconfig_deployment_strategy_us_west_2" {
  source = "../../modules/appconfig"
  providers = {
    aws = aws.prod-secondary
  }
}

module "services_us_west_1" {
  source    = "../../modules/services"
  providers = { aws = aws.prod-primary }
}

module "services_us_west_2" {
  source    = "../../modules/services"
  providers = { aws = aws.prod-secondary }
}