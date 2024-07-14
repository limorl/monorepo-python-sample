module "appconfig_app" {
  source   = "../appconfig-app"
  app_name = "${var.service_name}-service"
  env_name = var.stage
  tags     = var.tags
}

module "ecr_repository" {
  source              = "../ecr-repository"
  ecr_repository_name = var.service_name
  tags                = var.tags
}

