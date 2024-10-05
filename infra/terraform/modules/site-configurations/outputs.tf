output "table_arn" {
  description = "The ARN of the site-configurations table"
  value       = module.site_configurations_table.hash_table_arn
}