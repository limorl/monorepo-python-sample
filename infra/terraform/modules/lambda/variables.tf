variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "s3_key" {
  description = "The S3 key of the Lambda function's deployment package"
  type        = string
}

variable "handler" {
  description = "The function entrypoint in your code"
  type        = string
}

variable "runtime" {
  description = "The identifier of the function's runtime"
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., Dev, Test, Prod)"
  type        = string
  default     = "Dev" # You can set a default or make it required to specify
}

variable "subnet_ids" {
  description = "A list of subnet IDs to associate with the Lambda function in the VPC"
  type        = list(string)
}

variable "security_group_ids" {
  description = "A list of security group IDs to associate with the Lambda function in the VPC"
  type        = list(string)
}
