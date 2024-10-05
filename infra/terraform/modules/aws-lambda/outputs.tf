output "lambda_role_arn" {
  description = "The ARN of the Lambda execution role"
  value       = aws_iam_role.lambda_role.arn
}

output "lambda_role_id" {
  description = "The ID of the Lambda execution role"
  value       = aws_iam_role.lambda_role.id
}

output "lambda_security_group_id" {
  value = aws_security_group.lambda_sg.id
}
