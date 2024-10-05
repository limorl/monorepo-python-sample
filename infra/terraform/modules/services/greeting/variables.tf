variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

# Networking
variable "vpc_id" {
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

variable "vpc_endpoints_sg_id" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}