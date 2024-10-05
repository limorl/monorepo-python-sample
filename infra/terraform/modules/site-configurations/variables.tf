variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

variable "tags" {
  type    = map(string)
  default = {}
}