module "services" {
  source       = "./modules/service"
  service_name = "greeting"
  stage        = var.stage
}

module "services" {
  count        = var.stage != "prod" ? 1 : 0
  source       = "./modules/service"
  service_name = "test-appconfig"
  stage        = var.stage
}