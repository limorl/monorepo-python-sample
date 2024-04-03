output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.this.arn
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket created for the Lambda function's code"
  value       = aws_s3_bucket.lambda_function_bucket.bucket
}

output "lambda_execution_role_arn" {
  description = "The ARN of the IAM role assumed by the Lambda function"
  value       = aws_iam_role.lambda_execution_role.arn
}
