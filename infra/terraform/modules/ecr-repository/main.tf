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

resource "aws_ecr_repository_policy" "lambda_access" {
  repository = aws_ecr_repository.ecr_repository.name
  policy = file("${path.module}/lambda-access-policy.json")
}