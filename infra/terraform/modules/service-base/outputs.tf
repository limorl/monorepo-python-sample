output "appconfig_app_arn" {
  value = module.appconfig_app.appconfig_app_arn
}

output "ecr_repository_url" {
  value = module.ecr_repository.ecr_repository_url
}

output "ecr_repository_arn" {
  value = module.ecr_repository.ecr_repository_arn
}

output "lambda_role_arn" {
  value = module.lambda_function.lambda_role_arn
}

output "lambda_role_id" {
  value = module.lambda_function.lambda_role_id
}

output "lambda_security_group_id" {
  value = module.lambda_function.lambda_security_group_id
}

