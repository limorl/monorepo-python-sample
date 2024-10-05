<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.69.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_rds"></a> [rds](#module\_rds) | ../aws-rds | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_db_name"></a> [db\_name](#input\_db\_name) | The name of the database to create when the RDS instance is created | `string` | `"maindb"` | no |
| <a name="input_db_username"></a> [db\_username](#input\_db\_username) | The name of the database to create when the RDS instance is created | `string` | `"dbadmin"` | no |
| <a name="input_env"></a> [env](#input\_env) | The Environment (dev, staging prod) | `string` | n/a | yes |
| <a name="input_private_subnet_ids"></a> [private\_subnet\_ids](#input\_private\_subnet\_ids) | A list of private subnet IDs where resources can be placed | `list(string)` | n/a | yes |
| <a name="input_rds_allocated_storage"></a> [rds\_allocated\_storage](#input\_rds\_allocated\_storage) | The allocated storage for the RDS instance in gigabytes | `number` | `20` | no |
| <a name="input_rds_engine_version"></a> [rds\_engine\_version](#input\_rds\_engine\_version) | The engine version to use for the RDS instance | `string` | `"16.3"` | no |
| <a name="input_rds_instance_type"></a> [rds\_instance\_type](#input\_rds\_instance\_type) | The instance type of the RDS instance | `string` | `"db.t3.micro"` | no |
| <a name="input_ssm_instance_ami"></a> [ssm\_instance\_ami](#input\_ssm\_instance\_ami) | n/a | `string` | `null` | no |
| <a name="input_ssm_instance_region"></a> [ssm\_instance\_region](#input\_ssm\_instance\_region) | The region of the ssm instance | `string` | n/a | yes |
| <a name="input_ssm_instance_type"></a> [ssm\_instance\_type](#input\_ssm\_instance\_type) | The instance type of the EC2 instance | `string` | `"t3.micro"` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | A map of tags to add to all resources | `map(string)` | `{}` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | The ID of the VPC where resources will be created | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_maindb_credentials_secret_arn"></a> [maindb\_credentials\_secret\_arn](#output\_maindb\_credentials\_secret\_arn) | The ARN of maindb crdentials secret |
| <a name="output_rds_endpoint"></a> [rds\_endpoint](#output\_rds\_endpoint) | The endpoint of the RDS instance |
| <a name="output_rds_security_group_id"></a> [rds\_security\_group\_id](#output\_rds\_security\_group\_id) | n/a |
<!-- END_TF_DOCS -->