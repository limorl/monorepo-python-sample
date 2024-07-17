# General
variable "stage" {
  type    = string
  default = null
}

variable "aws_primary_region" {
  description = "Primary Region - for ECR, AppConfig, SecretsManager"
  type        = string
  default     = null
}

variable "aws_secondary_region" {
  description = "Secondary Region"
  type        = string
  default     = null
}