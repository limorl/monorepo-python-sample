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

variable "image_uri" {
  type = string
}

variable "tags" {
  type    = map(string)
  default = {}
}