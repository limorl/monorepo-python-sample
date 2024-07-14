variable "env_name" {
  type    = string
  default = null
}

variable "app_name" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}