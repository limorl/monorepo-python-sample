module "greeting_service" {
  source       = "../../service"
  service_name = "hello-world"
  stage        = var.stage
  tags         = var.tags
}