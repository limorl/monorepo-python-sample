module "greeting" {
  source = "./greeting"
  env    = var.env

  vpc_id              = var.vpc_id
  vpc_endpoints_sg_id = var.vpc_endpoints_sg_id
  private_subnet_ids  = var.private_subnet_ids

  tags = var.tags

  providers = {
    aws = aws
  }
}