module "greeting_service" {
  source       = "../../service"
  service_name = "greeting"
  stage        = var.stage
  tags         = var.tags
}