module "appconfig_app" {
  source   = "../appconfig-app"
  app_name = "test-appconfig-service"
  env_name = var.stage
  tags     = var.tags
}