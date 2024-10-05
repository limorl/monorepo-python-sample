data "aws_region" "current" {}

locals {
  region = data.aws_region.current.name
}

module "appconfig_app" {
  source   = "../aws-appconfig-app"
  app_name = "${var.service_name}-service"
  env_name = var.env

  tags = var.tags
}

module "ecr_repository" {
  source              = "../aws-ecr-repo"
  env                 = var.env
  ecr_repository_name = var.service_name

  tags = var.tags
}

module "lambda_function" {
  source = "../aws-lambda"

  env           = var.env
  function_name = var.service_name

  ecr_repository_url    = module.ecr_repository.ecr_repository_url
  ecr_repository_arn    = module.ecr_repository.ecr_repository_arn
  ecr_repository_policy = module.ecr_repository.ecr_repository_policy

  appconfig_app_arn = module.appconfig_app.appconfig_app_arn

  vpc_id               = var.vpc_id
  vpc_endpoints_sg_id  = var.vpc_endpoints_sg_id
  private_subnet_cidrs = var.private_subnet_cidrs

  tags = var.tags
}
