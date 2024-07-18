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

variable "tags" {
  type    = map(string)
  default = {}
}