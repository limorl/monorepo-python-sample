module "services" {
  source                      = "./modules/service"
  service_name                = "greeting"
  stage                       = var.stage
}