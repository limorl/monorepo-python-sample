output "main_vpc_id" {
  description = "The ID of the VPC"
  value       = local.main_vpc_id
}

output "main_private_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = local.main_private_subnet_ids
}

output "main_public_subnet_ids" {
  description = "The IDs of the private subnets"
  value       = local.main_public_subnet_ids
}

output "main_private_subnet_cidrs" {
  description = "The CIDR blocks of the private subnets"
  value       = module.main_vpc.private_subnets_cidr_blocks
}

output "main_vpc_endpoints_sg_id" {
  description = "The security group id for the VPC Endpoints of AppConfig, SecretsManager, SageMaker, Iot Core, DynamoDB"
  value       = aws_security_group.vpc_endpoints.id
}