output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.greeting_repo.repository_url
}

output "lambda_role_arn" {
  description = "The ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}