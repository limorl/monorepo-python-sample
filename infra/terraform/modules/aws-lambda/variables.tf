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

variable "function_name" {
  type    = string
  default = null
}

variable "ecr_repository_url" {
  description = "The URL of the ECR repository"
  type        = string
}

variable "ecr_repository_arn" {
  description = "The ARN of the ECR repository"
  type        = string
}

variable "ecr_repository_policy" {
  description = "The ECR repository policy"
  type        = any
  default     = null
}

variable "docker_tag" {
  description = "The tag of the Docker image to use"
  type        = string
  default     = "latest" # A place holder
}

variable "appconfig_app_arn" {
  description = "The ARN of the AppConfig app"
  type        = string
}

variable "tags" {
  type    = map(string)
  default = {}
}