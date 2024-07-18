output "lambda_role_arn" {
  description = "The ARN of the Lambda IAM role"
  value       = module.lambda_function.lambda_role_arn
}

output "ecr_repository_arn" {
  description = "The ARN of the ECR repository"
  value       = module.aws_ecr_repository.ecr_repository.arn
}
