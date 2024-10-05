# Add a rule to the SSM security group to allow outbound traffic to RDS
resource "aws_security_group_rule" "ssm_instance_to_rds" {
  type                     = "egress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  source_security_group_id = var.rds_security_group_id
  security_group_id        = var.ssm_instance_sg_id
}

# Add a rule to the RDS security group to allow inbound traffic from SSM Instance (EC2)
resource "aws_security_group_rule" "rds_from_ssm_instance" {
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = var.rds_security_group_id
  source_security_group_id = var.ssm_instance_sg_id
}
