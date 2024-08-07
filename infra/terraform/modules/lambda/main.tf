# we avoid creating the lambda itself using terraform for now, it will be created by SAM
# to use terraform we will need to use a dummy 'hello world' image
# resource "aws_lambda_function" "function" {
#   function_name = var.function_name
#   role          = aws_iam_role.lambda_role.arn
#   package_type  = "Image"
#   image_uri     = "${var.ecr_repository_url}:latest" # 'latest' is a placeholder, the image tag will be set when deploying using 'sam deploy'


#   lifecycle {
#     ignore_changes = [image_uri] # This allows SAM to update the image without Terraform interference
#   }

#   depends_on = [
#     aws_iam_role_policy_attachment.lambda_basic,
#     aws_iam_role_policy.lambda_ecr_policy,
#     var.ecr_repository_policy
#   ]

#   tags = merge(
#     var.tags,
#     {
#       Type = "aws_lambda_function"
#     },
#   )
# }

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 30
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

data "aws_iam_policy_document" "ecr_policy_document" {
  statement {
    effect = "Allow"
    actions = [
      "ecr:*"
      # "ecr:GetDownloadUrlForLayer",
      # "ecr:BatchGetImage",
      # "ecr:BatchCheckLayerAvailability",
      # "ecr:GetAuthorizationToken",
      # "ecr:DescribeRepositories",
      # "ecr:ListImages",
      # "ecr:DescribeImages"
    ]
    # resources = [var.ecr_repository_arn]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "lambda_ecr_policy" {
  name   = "${var.function_name}-lambda-ecr-policy"
  role   = aws_iam_role.lambda_role.id
  policy = data.aws_iam_policy_document.ecr_policy_document.json
}
