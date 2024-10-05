
# Output the SSM instance ID for use in tests or other modules

output "rds_security_group_id" {
  value = module.rds.rds_security_group_id
}

# Output the RDS endpoint for use in tests or other modules
output "rds_endpoint" {
  value       = module.rds.rds_endpoint
  description = "The endpoint of the RDS instance"
}

output "maindb_credentials_secret_arn" {
  description = "The ARN of maindb crdentials secret"
  value       = module.rds.maindb_credentials_secret_arn
}