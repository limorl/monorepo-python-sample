output "ecr_repository_url" {
  description = "The URL of the ECR repository"
  value       = aws_ecr_repository.ecr_repository.repository_url
}

output "ecr_repository_arn" {
  description = "The ARN of the ECR repository"
  value       = aws_ecr_repository.ecr_repository.arn
}

output "ecr_repository_policy" {
  description = "The ECR repository policy"
  value       = aws_ecr_repository_policy.lambda_access_policy
}
