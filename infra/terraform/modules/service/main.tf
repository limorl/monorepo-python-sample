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

module "lambda_function" {
  source             = "../lambda"
  function_name      = var.service_name
  ecr_repository_url = module.ecr_repository.ecr_repository_url
  ecr_repository_arn = module.ecr_repository.ecr_repository_arn
  ecr_repository_policy = module.ecr_repository.ecr_repository_policy
  tags               = var.tags
}
