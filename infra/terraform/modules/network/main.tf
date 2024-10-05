module "main_vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "main-vpc-${var.env}"
  cidr = "10.0.0.0/16"

  azs             = var.availability_zones
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway = false # CHANGE TO TRUE FOR KUNAK INGESTION AFTER VPC ENDPOINTS VERIFIED
  single_nat_gateway = false # CHANGE TO TRUE FOR KUNAK INGESTION AFTER VPC ENDPOINTS VERIFIED

  enable_vpn_gateway   = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    var.tags,
    { Name = "main-vpc-${var.env}" }
  )
}

locals {
  depends_on = [module.main_vpc]

  main_vpc_id                  = module.main_vpc.vpc_id
  main_private_subnet_ids      = module.main_vpc.private_subnets
  main_public_subnet_ids       = module.main_vpc.public_subnets
  main_private_route_table_ids = module.main_vpc.private_route_table_ids
  main_public_route_table_ids  = module.main_vpc.public_route_table_ids
}

# Private subnets

# resource "aws_subnet" "private" {
#   count             = length(var.private_subnet_cidrs)
#   vpc_id            = local.main_vpc_id
#   cidr_block        = var.private_subnet_cidrs[count.index]
#   availability_zone = data.aws_availability_zones.available.names[count.index]

#   tags = merge(
#     var.tags,
#     {
#       Group = "netowrk"
#       Name  = "private-subnet-${var.env}-${count.index + 1}"
#     },
#   )
# }

# resource "aws_route_table" "private" {
#   count  = length(var.private_subnet_cidrs)
#   vpc_id = local.main_vpc_id

#   tags = merge(
#     var.tags,
#     {
#       Group = "netowrk"
#       Name  = "private-route-table-${var.env}"
#     },
#   )
# }

# resource "aws_route_table_association" "private" {
#   count          = length(var.private_subnet_cidrs)
#   subnet_id      = aws_subnet.private[count.index].id
#   route_table_id = aws_route_table.private[count.index].id
# }

# Update security group created by default by the vpc module
resource "aws_default_security_group" "main_vpc_sg" {
  vpc_id = module.main_vpc.vpc_id

  tags = merge(
    var.tags,
    { Name = "main-vpc-sg-${var.env}" }
  )

  #   ingress {
  #     protocol         = -1
  #     self             = false
  #     from_port        = 0
  #     to_port          = 0
  #     cidr_blocks      = ["0.0.0.0/0"]
  #     ipv6_cidr_blocks = ["::/0"]
  #   }

  #   egress {
  #     protocol         = -1
  #     self             = false
  #     from_port        = 0
  #     to_port          = 0
  #     cidr_blocks      = ["0.0.0.0/0"]
  #     ipv6_cidr_blocks = ["::/0"]
  #   }
}

# Security Group for VPC Endpoints

resource "aws_security_group" "vpc_endpoints" {
  name        = "vpc-endpoints-sg-${var.env}"
  description = "Security group for VPC endpoints"
  vpc_id      = local.main_vpc_id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = var.private_subnet_cidrs
  }

  tags = merge(
    var.tags,
    {
      Group = "netowrk"
      Name  = "vpc-endpoints-sg-${var.env}"
    },
  )
}

# VPC Endpoints

resource "aws_vpc_endpoint" "appconfig" {
  vpc_id              = local.main_vpc_id
  service_name        = "com.amazonaws.${var.current_region}.appconfig"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = local.main_private_subnet_ids
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Group = "netowrk"
      Name  = "vpc-endpoint-appconfig-${var.env}"
    },
  )
}


resource "aws_vpc_endpoint" "appconfigdata" {
  vpc_id              = local.main_vpc_id
  service_name        = "com.amazonaws.${var.current_region}.appconfigdata"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = local.main_private_subnet_ids
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Group = "netowrk"
      Name  = "vpc-endpoint-appconfigdata-${var.env}"
    },
  )
}

resource "aws_vpc_endpoint" "secretsmanager" {
  vpc_id              = local.main_vpc_id
  service_name        = "com.amazonaws.${var.current_region}.secretsmanager"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = local.main_private_subnet_ids
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true

  tags = merge(
    var.tags,
    {
      Group = "netowrk"
      Name  = "vpc-endpoint-secretsmanager-${var.env}"
    },
  )
}
