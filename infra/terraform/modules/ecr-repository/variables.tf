variable "ecr_name" {
  description = "The ECR registry name"
  type        = string
  default     = null
}

variable "ecr_repository_name" {
  type    = string
  default = null
}

variable "image_mutability" {
  type    = string
  default = "MUTABLE"
}

variable "scan_on_push" {
  type    = bool
  default = true
}

variable "encrypt_type" {
  type    = string
  default = "KMS"
}

variable "tags" {
  type    = map(string)
  default = {}
}