module "appconfig_deployment_strategy_us_east_1" {
    source = "../../modules/appconfig"
    providers = {
      aws = aws.primary
    }
}

module "services_us_east_1" {
  source               = "../../modules/services"
  providers            = { aws = aws.primary }
}