module "rds" {
  source = "../aws-rds"

  env                = var.env
  vpc_id             = var.vpc_id
  private_subnet_ids = var.private_subnet_ids
  instance_type      = var.rds_instance_type
  allocated_storage  = var.rds_allocated_storage
  db_username        = var.db_username
  db_name            = var.db_name

  tags = var.tags
}

