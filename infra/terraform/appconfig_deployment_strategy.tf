# We're creating all types of deployments on all environments 

resource "aws_appconfig_deployment_strategy" "appconfig_deployment_strategy_dev" {
  name                           = "dev-deployment-strategy"
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = {
    Stage = "dev"
  }
}

resource "aws_appconfig_deployment_strategy" "appconfig_deployment_strategy_staging" {
  name                           = "staging-deployment-strategy"
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = {
    Stage = "staging"
  }
}

resource "aws_appconfig_deployment_strategy" "appconfig_deployment_strategy_prod" {
  name                           = "prod-deployment-strategy"
  deployment_duration_in_minutes = 10
  final_bake_time_in_minutes     = 2
  growth_factor                  = 20
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = {
    Stage = "prod"
  }
}
