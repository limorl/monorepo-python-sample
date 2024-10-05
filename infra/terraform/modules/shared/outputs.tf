output "env" {
  value = var.env
}

output "primary_region" {
  value = var.primary_region
}

output "current_region" {
  value = var.current_region
}

output "global_key" {
  value = var.global_key
}

# Networking
output "main_vpc_private_subnet_cidrs" {
  value = module.network.main_private_subnet_cidrs
}

# SSM
# We use a specific AMI ID to avoid instance replacement which will require updating SSM_INSTANCE_ID per environment
#output "ssm_instance_ami" {
#  value = module.ssm_instance.id
#}
