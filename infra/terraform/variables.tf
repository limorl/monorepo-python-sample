# General

variable "aws_primary_region" {
    description = "Primary Region - for ECR, AppConfig, SecretsManager"
    type        = string
    default     = null
}

variable "aws_region" {
    description = "Region to deploy to"
    type        = string
    default     = null
}

variable "stage" {
    type        = string
    default     = null
}