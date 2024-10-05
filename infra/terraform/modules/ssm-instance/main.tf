resource "aws_security_group" "ssm_instance_sg" {
  name   = "ssm-instance-sg-${var.env}"
  vpc_id = var.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "ssm-instance-sg-${var.env}"
    },
  )
}

data "aws_subnet" "ssm_instance_private" {
  id = var.private_subnet_ids[0]
}

resource "aws_instance" "ssm_instance" {
  ami           = var.ssm_instance_ami
  instance_type = var.ssm_instance_type
  subnet_id     = data.aws_subnet.ssm_instance_private.id

  vpc_security_group_ids = [aws_security_group.ssm_instance_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.ssm_profile.name

  tags = merge(
    var.tags,
    {
      Name = "ssm-instance-${var.env}"
    },
  )
}

resource "aws_iam_role" "ssm_role" {
  name = "ssm-role-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ssm_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  role       = aws_iam_role.ssm_role.name
}

resource "aws_iam_instance_profile" "ssm_profile" {
  name = "ssm-instance-profile-${var.env}"
  role = aws_iam_role.ssm_role.name
}


resource "aws_security_group" "vpc_endpoint_ssm_sg" {
  name        = "vpc-endpoint-ssm-sg-${var.env}"
  description = "Security group for SSM VPC endpoints"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTPS from SSM instance subnet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [data.aws_subnet.ssm_instance_private.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(
    var.tags,
    {
      Name = "vpc-endpoint-ssm-sg-${var.env}"
    },
  )
}

resource "aws_vpc_endpoint" "ssm" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.ssm"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [data.aws_subnet.ssm_instance_private.id]
  security_group_ids  = [aws_security_group.vpc_endpoint_ssm_sg.id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Name = "vpc-endpoint-ssm-${var.env}"
    },
  )
}

resource "aws_vpc_endpoint" "ec2messages" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.ec2messages"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [data.aws_subnet.ssm_instance_private.id]
  security_group_ids  = [aws_security_group.vpc_endpoint_ssm_sg.id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Name = "vpc-endpoint-ec2messages-${var.env}"
    },
  )
}

resource "aws_vpc_endpoint" "ssmmessages" {
  vpc_id              = var.vpc_id
  service_name        = "com.amazonaws.${var.region}.ssmmessages"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [data.aws_subnet.ssm_instance_private.id]
  security_group_ids  = [aws_security_group.vpc_endpoint_ssm_sg.id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Name = "vpc_endpoint-ssmmessages-${var.env}"
    },
  )
}