# We avoid creating the lambda itself using terraform since we create and manage lambda deployments using SAM

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

data "aws_vpc" "main" {
  id = var.vpc_id
}

# VPC configuration and security groups created by Terraform
resource "aws_security_group" "lambda_sg" {
  name        = "${var.function_name}-lambda-sg-${var.env}"
  description = "Security group for Lambda"
  vpc_id      = var.vpc_id

  # Egress rule to allow the lambda communicate with external and internal resources, such as ops geneie, kunak api, etc.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Ingress rule to allow inbound access to lambda from within the VPC
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [data.aws_vpc.main.cidr_block] # Allow traffic from the entire vpc
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.function_name}-lambda-sg-${var.env}"
    },
  )
}


# stateUpdate Lambda Security Group to allow access to VPC endpoints
resource "aws_security_group_rule" "lambda_to_vpc_endpoints" {
  type                     = "egress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = aws_security_group.lambda_sg.id
  source_security_group_id = var.vpc_endpoints_sg_id
}

# Allow inbound traffic from Lambda to VPC endpoints
resource "aws_security_group_rule" "vpc_endpoints_from_lambda" {
  type                     = "ingress"
  from_port                = 443
  to_port                  = 443
  protocol                 = "tcp"
  security_group_id        = var.vpc_endpoints_sg_id
  source_security_group_id = aws_security_group.lambda_sg.id
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/${var.env}/aws/lambda/${var.function_name}"
  retention_in_days = 30
}

resource "aws_iam_role" "lambda_role" {
  name               = "${var.function_name}-lambda-role-${var.env}"
  assume_role_policy = file("${path.module}/assume-role-policy.json")

  tags = var.tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

resource "aws_iam_role_policy" "lambda_shared_policy" {
  name = "lambda-shared-policy-${var.env}"
  role = aws_iam_role.lambda_role.id

  policy = templatefile("${path.module}/lambda-shared-policy.tftpl", {
    region               = data.aws_region.current.name
    ecr_repository_arn   = var.ecr_repository_arn
    lambda_log_group_arn = aws_cloudwatch_log_group.lambda_log_group.arn
  })
}
