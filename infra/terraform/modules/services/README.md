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
| <a name="module_breeze"></a> [breeze](#module\_breeze) | ./breeze | n/a |
| <a name="module_greeting"></a> [greeting](#module\_greeting) | ./greeting | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_env"></a> [env](#input\_env) | The Environment (dev, staging prod) | `string` | n/a | yes |
| <a name="input_maindb_credentials_secret_arn"></a> [maindb\_credentials\_secret\_arn](#input\_maindb\_credentials\_secret\_arn) | The ARN of maindb crdentials secret | `string` | n/a | yes |
| <a name="input_private_subnet_cidrs"></a> [private\_subnet\_cidrs](#input\_private\_subnet\_cidrs) | CIDR blocks of private subnets | `list(string)` | `[]` | no |
| <a name="input_private_subnet_ids"></a> [private\_subnet\_ids](#input\_private\_subnet\_ids) | The IDs of the private subnets | `list(string)` | n/a | yes |
| <a name="input_rds_security_group_id"></a> [rds\_security\_group\_id](#input\_rds\_security\_group\_id) | The ID of the RDS MainDB Security Group | `string` | n/a | yes |
| <a name="input_site_configurations_table_arn"></a> [site\_configurations\_table\_arn](#input\_site\_configurations\_table\_arn) | The ARN of the site-configurations DynamoDb table | `string` | n/a | yes |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(string)` | `{}` | no |
| <a name="input_timestream_database_arn"></a> [timestream\_database\_arn](#input\_timestream\_database\_arn) | The ARN of the Timestream table | `string` | n/a | yes |
| <a name="input_vpc_endpoints_sg_id"></a> [vpc\_endpoints\_sg\_id](#input\_vpc\_endpoints\_sg\_id) | n/a | `string` | `null` | no |
| <a name="input_vpc_id"></a> [vpc\_id](#input\_vpc\_id) | The ID of the VPC where the EC2 instance will be created | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_services_primary_outputs"></a> [services\_primary\_outputs](#output\_services\_primary\_outputs) | n/a |
<!-- END_TF_DOCS -->