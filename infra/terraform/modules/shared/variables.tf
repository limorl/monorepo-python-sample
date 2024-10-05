# General
variable "env" {
  type    = string
  default = null
}

variable "primary_region" {
  description = "Primary Region - for ECR, AppConfig, SecretsManager"
  type        = string
  default     = null
}

variable "current_region" {
  description = "Current Region for deployed resource"
  type        = string
  default     = null
}

variable "global_key" {
  description = "Unique key to be used for global resource name to create uniqueness"
  type        = string
  default     = null
}

# Networking
variable "availability_zones" {
  type    = list(string)
  default = null
}

# SSM
# We use a specific AMI ID to avoid instance replacement which will require updating SSM_INSTANCE_ID per environment
# variable "ssm_instance_ami" {
#   type    = string
#   default = null
# }

# variable "ssm_instance_type" {
#   description = "The instance type of the EC2 SSM instance"
#   type        = string
#   default     = "null"
# }