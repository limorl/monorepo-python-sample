variable "stage" {
  type    = string
  default = null
}

variable "service_name" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}