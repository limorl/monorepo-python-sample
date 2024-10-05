output "greeting_appconfig_app_arn" {
  value = module.greeting_service.appconfig_app_arn
}

output "greeting_ecr_repository_url" {
  value = module.greeting_service.ecr_repository_url
}

output "greeting_ecr_repository_arn" {
  value = module.greeting_service.ecr_repository_arn
}

output "greeting_lambda_role_arn" {
  value = module.greeting_service.lambda_role_arn
}

output "greeting_lambda_role_id" {
  value = module.greeting_service.lambda_role_id
}

output "greeting_lambda_security_group_id" {
  value = module.greeting_service.lambda_security_group_id
}

