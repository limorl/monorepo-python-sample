locals {
  service_name = "greeting"
}

module "greeting_service" {
  source = "../../service-base"

  env                  = var.env
  service_name         = local.service_name
  vpc_id               = var.vpc_id 
  vpc_endpoints_sg_id  = var.vpc_endpoints_sg_id
  private_subnet_cidrs = var.private_subnet_cidrs

  providers = {
    aws = aws
  }

  tags = merge(
    var.tags,
    { Service = local.service_name }
  )
}