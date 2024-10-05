
variable "env" {
  description = "The Environment (dev, staging prod)"
  type        = string
}

variable "vpc_id" {
  description = "The ID of the VPC where resources will be created"
  type        = string
}

variable "private_subnet_ids" {
  description = "A list of private subnet IDs where resources can be placed"
  type        = list(string)

  validation {
    condition     = length(var.private_subnet_ids) > 0
    error_message = "At least one private subnet ID must be provided."
  }
}

variable "ssm_instance_region" {
  description = "The region of the ssm instance"
  type        = string
}

variable "ssm_instance_type" {
  description = "The instance type of the EC2 instance"
  type        = string
  default     = "t3.micro"
}

variable "ssm_instance_ami" {
  type    = string
  default = null
}

variable "rds_instance_type" {
  description = "The instance type of the RDS instance"
  type        = string
  default     = "db.t3.micro"
}

variable "rds_allocated_storage" {
  description = "The allocated storage for the RDS instance in gigabytes"
  type        = number
  default     = 20
}

variable "rds_engine_version" {
  description = "The engine version to use for the RDS instance"
  type        = string
  default     = "16.3"
}

variable "db_username" {
  description = "The name of the database to create when the RDS instance is created"
  type        = string
  default     = "dbadmin"
}


variable "db_name" {
  description = "The name of the database to create when the RDS instance is created"
  type        = string
  default     = "maindb"
}


variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default     = {}
}