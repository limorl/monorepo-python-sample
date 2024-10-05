variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

variable "current_region" {
  description = "Current Region for deployed resource"
  type        = string
  default     = null
}

variable "availability_zones" {
  type    = list(string)
  default = null
}

variable "private_subnet_cidrs" {
  description = "The CIDR blocks of the private subnets to be created. They are determined based on the public subnet blocks of the default VPC"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnet_cidrs" {
  description = "The CIDR blocks of the private subnets to be created. They are determined based on the public subnet blocks of the default VPC"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "tags" {
  type    = map(string)
  default = {}
}
