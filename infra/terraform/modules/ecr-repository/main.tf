resource "aws_ecr_repository" "ecr_repository" {
  name                 = var.ecr_repository_name
  image_tag_mutability = var.image_mutability

  encryption_configuration {
    encryption_type = var.encrypt_type
  }

  image_scanning_configuration {
    scan_on_push = var.scan_on_push
  }

  tags = merge(
    var.tags,
    {
      Type = "ecr_repository"
    },
  )
}

# resource "aws_ecr_repository_policy" "lambda_access_policy" {
#   repository = aws_ecr_repository.ecr_repository.name
#   policy     = file("${path.module}/lambda-access-policy.json")
#   lifecycle {
#     ignore_changes = [policy]
#   }
# }

resource "aws_ecr_repository_policy" "lambda_access_policy" {
  repository = aws_ecr_repository.ecr_repository.name
  depends_on = [aws_ecr_repository.ecr_repository]
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "LambdaECRImageRetrievalPolicy"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
      }
    ]
  })
}

# Debug policy file
output "policy_content" {
  value = file("${path.module}/lambda-access-policy.json")
}