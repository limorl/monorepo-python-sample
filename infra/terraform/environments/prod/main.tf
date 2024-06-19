resource "aws_appconfig_deployment_strategy" "deployment_strategy_primary" {
  name                           = "prod-deployment-strategy"
  provider                       = aws.prod-primary              
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = {
      Type = "appconfig_deployment_strategy"
  }
}


module "services_primary" {
  source    = "../../modules/services"
  providers = { aws = aws.prod-primary }
}

module "services_secondary" {
  source    = "../../modules/services"
  providers = { aws = aws.prod-secondary }
}