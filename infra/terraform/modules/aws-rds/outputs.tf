
output "rds_endpoint" {
  value = aws_db_instance.main.endpoint
}

output "rds_security_group_id" {
  value = aws_security_group.rds.id
}

output "db_name" {
  description = "The name of the default database created on the RDS instance"
  value       = aws_db_instance.main.db_name
}

output "db_secret_name" {
  description = "The name of the Secrets Manager secret containing the database credentials"
  value       = aws_secretsmanager_secret.rds_credentials.name
}

output "maindb_credentials_secret_arn" {
  description = "The ARN of maindb crdentials secret"
  value       = aws_secretsmanager_secret.rds_credentials.arn
}
