variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where the RDS instance will be created"
  type        = string
}

variable "private_subnet_ids" {
  description = "A list of private subnet IDs where the RDS instance can be placed"
  type        = list(string)
}

variable "instance_type" {
  description = "The instance type of the RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "allocated_storage" {
  description = "The allocated storage in gigabytes"
  type        = number
  default     = 20
}

variable "engine" {
  type    = string
  default = "postgres"
}

variable "engine_version" {
  description = "The engine version to use"
  type        = string
  default     = "16.3"
}

variable "db_username" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
  default     = "dbadmin"
}

variable "db_name" {
  description = "The name of the database to create when the DB instance is created"
  type        = string
  default     = "maindb"
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}