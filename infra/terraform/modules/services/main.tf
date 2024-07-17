module "greeting" {
  source = "./greeting"
  stage  = var.stage
  tags   = var.tags
}