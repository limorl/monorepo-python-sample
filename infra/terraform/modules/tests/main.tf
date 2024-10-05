module "appconfig_test_app" {
  source   = "../aws-appconfig-app"
  app_name = "test-service"
  env_name = var.env
  tags     = var.tags
}