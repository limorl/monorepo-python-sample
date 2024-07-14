module "appconfig_app" {
  source   = "../appconfig_app"
  app_name = "test-service"
  env_name = var.stage
  tags     = var.tags
}