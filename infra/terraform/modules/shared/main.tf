# For now, we're deploying in a single region. To support a secondary region, duplicate the resources,
# replace the suffix -primary with -secondary and use aws.dev-secondary provider

module "network" {
  source             = "../network"
  env                = var.env
  current_region     = var.current_region
  availability_zones = var.availability_zones
}

# Added RDS Postgress infra for the example, not yet used

# module "maindb" {
#   source              = "../maindb"
#   depends_on          = [module.network]
#   env                 = var.env
#   vpc_id              = module.network.vpc_id
#   private_subnet_ids  = module.network.private_subnet_ids
#   ssm_instance_region = var.primary_region
#   ssm_instance_ami    = var.ssm_instance_ami
# }


# module "ssm_instance" {
#   source     = "../ssm-instance"
#   depends_on = [module.network, module.maindb]

#   env                = var.env
#   region             = var.current_region
#   ssm_instance_type  = var.ssm_instance_type
#   ssm_instance_ami   = var.ssm_instance_ami
#   vpc_id             = module.network.vpc_id
#   private_subnet_ids = module.network.private_subnet_ids
# }

# module "ssm_tunnel" {
#   source     = "../ssm-tunnel"
#   depends_on = [module.maindb, module.ssm_instance]

#   rds_security_group_id = module.maindb.rds_security_group_id
#   ssm_instance_sg_id    = module.ssm_instance.ssm_instance_sg_id
# }

module "services" {
  source     = "../services"
  depends_on = [module.network]

  env                 = var.env
  vpc_id              = module.network.main_vpc_id
  private_subnet_ids  = module.network.main_private_subnet_ids
  vpc_endpoints_sg_id = module.network.main_vpc_endpoints_sg_id
  # rds_security_group_id         = module.maindb.rds_security_group_id
  # maindb_credentials_secret_arn = module.maindb.maindb_credentials_secret_arn

  providers = {
    aws = aws
  }
}

# For now, we are using the same app-config deployment strategy for dev, staging and prod
# In the future we may consider gradual deployment stragey for prod
resource "aws_appconfig_deployment_strategy" "deployment_strategy" {
  name                           = "deployment-strategy-${var.env}"
  deployment_duration_in_minutes = 0
  final_bake_time_in_minutes     = 0
  growth_factor                  = 100
  growth_type                    = "LINEAR"
  replicate_to                   = "NONE"
}
