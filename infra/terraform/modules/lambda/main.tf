resource "aws_lambda_function" "function" {
  function_name = var.function_name
  role          = aws_iam_role.lambda_role.arn
  package_type  = "Image"
  image_uri     = var.image_uri
}

resource "aws_iam_role" "lambda_role" {
  name               = "${var.function_name}-lambda-role"
  assume_role_policy = file("${path.module}/assume-role-policy.json")
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_role_policy" "lambda_appconfig_secretsmanager_policy" {
  name = "${var.function_name}-lambda-appconfig-secretsmanager-policy"
  role = aws_iam_role.lambda_role.id

  policy = file("${path.module}/appconfig-secretesmanager-policy.json")
}
