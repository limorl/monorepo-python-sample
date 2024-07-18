
resource "aws_lambda_function" "function" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = "${var.ecr_repository_url}:${var.docker_tag}"

  tags = merge(
    var.tags,
    {
      Type = "aws_lambda_function"
    },
  )
}

resource "aws_iam_role" "lambda_role" {
  name               = "${var.function_name}-lambda-role"
  assume_role_policy = file("${path.module}/assume-role-policy.json")

  tags = merge(
    var.tags,
    {
      Type = "aws_iam_role"
    },
  )
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_role_policy" "lambda_appconfig_secretsmanager_policy" {
  name   = "${var.function_name}-lambda-appconfig-secretsmanager-policy"
  role   = aws_iam_role.lambda_role.id
  policy = file("${path.module}/appconfig-secretesmanager-policy.json")
}

data "aws_iam_policy_document" "ecr_access_policy_document" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability"
    ]
    resources = [var.ecr_repository_arn]
  }
}

resource "aws_iam_policy" "ecr_access" {
  name        = "${var.function_name}-lambda-ecr-access"
  path        = "/"
  description = "IAM policy for accessing ECR from Lambda"
  policy      = data.aws_iam_policy_document.ecr_access_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_ecr" {
  policy_arn = aws_iam_policy.ecr_access.arn
  role       = aws_iam_role.lambda_role.name
}
