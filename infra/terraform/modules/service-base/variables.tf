variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

variable "vpc_id" {
  type    = string
  default = null
}

variable "vpc_endpoints_sg_id" {
  type    = string
  default = null
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks of private subnets"
  type        = list(string)
  default     = []
}

variable "service_name" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}