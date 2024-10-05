data "aws_vpc" "default" {
  id = var.vpc_id
}

resource "aws_security_group" "rds" {
  name   = "rds-sg-${var.env}"
  vpc_id = var.vpc_id

  # Ingress rule for ECS SSM Instance will be added after rds module is created

  # Egress rule to limit outbound connection within vpc
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }

  tags = merge(
    var.tags,
    {
      Group = "rds/${var.engine}/${var.db_name}"
      Name  = "rds-sg-${var.env}"
    },
  )
}

resource "aws_db_subnet_group" "main" {
  name       = "${var.db_name}-subnet-group-${var.env}"
  subnet_ids = var.private_subnet_ids
}

resource "aws_db_instance" "main" {
  identifier             = "${var.db_name}-${var.env}"
  db_name                = var.db_name
  engine                 = var.engine
  engine_version         = var.engine_version
  instance_class         = var.instance_type
  allocated_storage      = 20
  storage_type           = "gp2"
  username               = var.db_username
  password               = random_password.db_password.result
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot    = true

  lifecycle {
    prevent_destroy = true
  }

  tags = merge(
    var.tags,
    {
      Group = "rds/${var.engine}/${var.db_name}"
  })
}

resource "random_password" "db_password" {
  length  = 16
  special = false
}

resource "aws_secretsmanager_secret" "rds_credentials" {
  description = "Credentials for RDS Postgress main db"
  name        = "${var.env}/rds/credentials/${aws_db_instance.main.identifier}"

  tags = merge(
    {
      Group = "rds/${var.engine}/${var.db_name}"
    }
  )
}

resource "aws_secretsmanager_secret_version" "rds_credentials" {
  secret_id = aws_secretsmanager_secret.rds_credentials.id
  secret_string = jsonencode({
    engine   = aws_db_instance.main.engine
    username = aws_db_instance.main.username
    password = random_password.db_password.result
    host     = aws_db_instance.main.address
    port     = 5432
    dbname   = aws_db_instance.main.db_name
  })
}
