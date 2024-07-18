output "lambda_role_arn" {
  description = "The ARN of the Lambda IAM role"
  value       = module.lambda_function.lambda_role_arn
}
