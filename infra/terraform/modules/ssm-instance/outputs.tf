
output "ssm_instance_id" {
  description = "The ID of the EC2 instance"
  value       = aws_instance.ssm_instance.id
}

output "ssm_private_ip" {
  description = "The private IP address of the EC2 instance"
  value       = aws_instance.ssm_instance.private_ip
}

output "ssm_role_arn" {
  description = "The ARN of the IAM role used for SSM"
  value       = aws_iam_role.ssm_role.arn
}

output "ssm_instance_sg_id" {
  description = "The ID of the security group associated with the EC2 SSM instance"
  value       = aws_security_group.ssm_instance_sg.id
}