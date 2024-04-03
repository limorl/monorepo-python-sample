resource "aws_s3_bucket" "lambda_function_bucket" {
  bucket_prefix = "${var.function_name}-"
  acl           = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "Lambda Function Bucket"
    Environment = var.environment
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.function_name}_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Principal = { Service = "lambda.amazonaws.com" }
      Effect = "Allow"
    }]
  })
}

resource "aws_lambda_function" "this" {
  function_name = var.function_name

  s3_bucket = aws_s3_bucket.lambda_function_bucket.bucket
  s3_key    = var.s3_key

  handler = var.handler
  runtime = var.runtime
  role    = aws_iam_role.lambda_execution_role.arn

  vpc_config {
    subnet_ids         = var.subnet_ids
    security_group_ids = var.security_group_ids
  }
}


