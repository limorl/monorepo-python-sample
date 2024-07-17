variable "stage" {
  type    = string
  default = null
}

variable "function_name" {
  type    = string
  default = null
}

variable "lambda_timeout" {
  type    = number
  default = 10
}

variable "ecr_repository_url" {
  description = "The URL of the ECR repository"
  type        = string
}

variable "image_tag" {
  description = "The tag of the Docker image to use"
  type        = string
  default     = "latest"
}

variable "tags" {
  type    = map(string)
  default = {}
}