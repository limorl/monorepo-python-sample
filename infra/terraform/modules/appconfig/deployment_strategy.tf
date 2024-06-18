resource "aws_appconfig_deployment_strategy" "dev_deployment_strategy" {
  count                          = var.stage == "dev" ? 1 : 0
  name                           = "dev-deployment-strategy"
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = merge(
    var.tags,
    {
      Type = "appconfig_deployment_strategy"
    },
  )
}

resource "aws_appconfig_deployment_strategy" "staging_deployment_strategy" {
  count                          = var.stage == "staging" ? 1 : 0
  name                           = "staging-deployment-strategy"
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = merge(
    var.tags,
    {
      Type = "appconfig_deployment_strategy"
    },
  )
}

resource "aws_appconfig_deployment_strategy" "prod_deployment_strategy" {
  count                          = var.stage == "prod" ? 1 : 0
  name                           = "prod-deployment-strategy"
  deployment_duration_in_minutes = 10
  final_bake_time_in_minutes     = 2
  growth_factor                  = 20
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"

  tags = merge(
    var.tags,
    {
      Type = "appconfig_deployment_strategy"
    },
  )
}
