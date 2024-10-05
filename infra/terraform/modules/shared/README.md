<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.69.0 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | ~> 5.69.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_iot_rules"></a> [iot\_rules](#module\_iot\_rules) | ../iot-rules | n/a |
| <a name="module_maindb"></a> [maindb](#module\_maindb) | ../maindb | n/a |
| <a name="module_ml-models"></a> [ml-models](#module\_ml-models) | ../ml-models | n/a |
| <a name="module_network"></a> [network](#module\_network) | ../network | n/a |
| <a name="module_recent_data"></a> [recent\_data](#module\_recent\_data) | ../recent-data | n/a |
| <a name="module_secrets"></a> [secrets](#module\_secrets) | ../secrets | n/a |
| <a name="module_services"></a> [services](#module\_services) | ../services | n/a |
| <a name="module_site_configurations"></a> [site\_configurations](#module\_site\_configurations) | ../site-configurations | n/a |
| <a name="module_ssm_instance"></a> [ssm\_instance](#module\_ssm\_instance) | ../ssm-instance | n/a |
| <a name="module_ssm_tunnel"></a> [ssm\_tunnel](#module\_ssm\_tunnel) | ../ssm-tunnel | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_appconfig_deployment_strategy.deployment_strategy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appconfig_deployment_strategy) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_current_region"></a> [current\_region](#input\_current\_region) | Current Region for deployed resource | `string` | `null` | no |
| <a name="input_env"></a> [env](#input\_env) | General | `string` | `null` | no |
| <a name="input_global_key"></a> [global\_key](#input\_global\_key) | Unique key to be used for global resource name to create uniqueness | `string` | `null` | no |
| <a name="input_ml_model_endpoint_instance_type"></a> [ml\_model\_endpoint\_instance\_type](#input\_ml\_model\_endpoint\_instance\_type) | ML | `string` | `null` | no |
| <a name="input_primary_region"></a> [primary\_region](#input\_primary\_region) | Primary Region - for ECR, AppConfig, SecretsManager | `string` | `null` | no |
| <a name="input_private_subnet_cidrs"></a> [private\_subnet\_cidrs](#input\_private\_subnet\_cidrs) | CIDR blocks of private subnets | `list(string)` | `[]` | no |
| <a name="input_ssm_instance_ami"></a> [ssm\_instance\_ami](#input\_ssm\_instance\_ami) | SSM We use a specific AMI ID to avoid instance replacement which will require updating SSM\_INSTANCE\_ID per environment | `string` | `null` | no |
| <a name="input_ssm_instance_type"></a> [ssm\_instance\_type](#input\_ssm\_instance\_type) | The instance type of the EC2 SSM instance | `string` | `"null"` | no |
| <a name="input_vpc_endpoint_timestream_query_cell"></a> [vpc\_endpoint\_timestream\_query\_cell](#input\_vpc\_endpoint\_timestream\_query\_cell) | The query CELL of the timestream vpc endpoint, which may vary based on region | `string` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_current_region"></a> [current\_region](#output\_current\_region) | n/a |
| <a name="output_env"></a> [env](#output\_env) | n/a |
| <a name="output_global_key"></a> [global\_key](#output\_global\_key) | n/a |
| <a name="output_primary_region"></a> [primary\_region](#output\_primary\_region) | n/a |
| <a name="output_private_subnet_cidrs"></a> [private\_subnet\_cidrs](#output\_private\_subnet\_cidrs) | Networking |
| <a name="output_ssm_instance_ami"></a> [ssm\_instance\_ami](#output\_ssm\_instance\_ami) | SSM We use a specific AMI ID to avoid instance replacement which will require updating SSM\_INSTANCE\_ID per environment |
<!-- END_TF_DOCS -->