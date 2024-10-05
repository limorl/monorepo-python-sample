# General

variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

# Networking

variable "vpc_id" {
  description = "The ID of the VPC where the EC2 instance will be created"
  type        = string
}

variable "vpc_endpoints_sg_id" {
  type    = string
  default = null
}

variable "private_subnet_ids" {
  description = "The IDs of the private subnets"
  type        = list(string)
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks of private subnets"
  type        = list(string)
  default     = []
}

# RDS MainDB

# variable "rds_security_group_id" {
#   description = "The ID of the RDS MainDB Security Group"
#   type        = string
# }

# variable "maindb_credentials_secret_arn" {
#   description = "The ARN of maindb crdentials secret"
#   type        = string
# }

# # DynamoDB
# variable "site_configurations_table_arn" {
#   description = "The ARN of the site-configurations DynamoDb table"
#   type        = string
# }

variable "tags" {
  type    = map(string)
  default = {}
}