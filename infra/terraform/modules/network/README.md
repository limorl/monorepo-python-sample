<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.69.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.62.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_main_vpc"></a> [main\_vpc](#module\_main\_vpc) | terraform-aws-modules/vpc/aws | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_default_security_group.main_vpc_sg](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/default_security_group) | resource |
| [aws_security_group.vpc_endpoints](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/security_group) | resource |
| [aws_vpc_endpoint.appconfig](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_endpoint) | resource |
| [aws_vpc_endpoint.appconfigdata](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_endpoint) | resource |
| [aws_vpc_endpoint.secretsmanager](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc_endpoint) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_availability_zones"></a> [availability\_zones](#input\_availability\_zones) | n/a | `list(string)` | `null` | no |
| <a name="input_current_region"></a> [current\_region](#input\_current\_region) | Current Region for deployed resource | `string` | `null` | no |
| <a name="input_env"></a> [env](#input\_env) | The Environment (dev, staging prod) | `string` | n/a | yes |
| <a name="input_private_subnet_cidrs"></a> [private\_subnet\_cidrs](#input\_private\_subnet\_cidrs) | The CIDR blocks of the private subnets to be created. They are determined based on the public subnet blocks which somes with the default VPC | `list(string)` | <pre>[<br>  "10.0.1.0/24",<br>  "10.0.2.0/24",<br>  "10.0.3.0/24"<br>]</pre> | no |
| <a name="input_public_subnet_cidrs"></a> [public\_subnet\_cidrs](#input\_public\_subnet\_cidrs) | The CIDR blocks of the private subnets to be created. They are determined based on the public subnet blocks which somes with the default VPC | `list(string)` | <pre>[<br>  "10.0.101.0/24",<br>  "10.0.102.0/24",<br>  "10.0.103.0/24"<br>]</pre> | no |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_main_private_subnet_cidrs"></a> [main\_private\_subnet\_cidrs](#output\_main\_private\_subnet\_cidrs) | The CIDR blocks of the private subnets |
| <a name="output_main_private_subnet_ids"></a> [main\_private\_subnet\_ids](#output\_main\_private\_subnet\_ids) | The IDs of the private subnets |
| <a name="output_main_public_subnet_ids"></a> [main\_public\_subnet\_ids](#output\_main\_public\_subnet\_ids) | The IDs of the private subnets |
| <a name="output_main_vpc_endpoints_sg_id"></a> [main\_vpc\_endpoints\_sg\_id](#output\_main\_vpc\_endpoints\_sg\_id) | The security group id for the VPC Endpoints of AppConfig, SecretsManager, SageMaker, Iot Core, DynamoDB |
| <a name="output_main_vpc_id"></a> [main\_vpc\_id](#output\_main\_vpc\_id) | The ID of the VPC |
<!-- END_TF_DOCS -->