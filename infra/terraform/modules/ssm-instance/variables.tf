
variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

variable "region" {
  description = "The region of the instance"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the EC2 instance will be created"
  type        = string
}

variable "private_subnet_ids" {
  description = "The IDs of the private subnets"
  type        = list(string)
}

variable "ssm_instance_type" {
  description = "The instance type of the EC2 SSM instance"
  type        = string
  default     = "null"
}

variable "ssm_instance_ami" {
  type    = string
  default = null
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}
