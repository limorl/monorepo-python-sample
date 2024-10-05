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
| <a name="module_network"></a> [network](#module\_network) | ../network | n/a |
| <a name="module_services"></a> [services](#module\_services) | ../services | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_appconfig_deployment_strategy.deployment_strategy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/appconfig_deployment_strategy) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_availability_zones"></a> [availability\_zones](#input\_availability\_zones) | Networking | `list(string)` | `null` | no |
| <a name="input_current_region"></a> [current\_region](#input\_current\_region) | Current Region for deployed resource | `string` | `null` | no |
| <a name="input_env"></a> [env](#input\_env) | General | `string` | `null` | no |
| <a name="input_global_key"></a> [global\_key](#input\_global\_key) | Unique key to be used for global resource name to create uniqueness | `string` | `null` | no |
| <a name="input_primary_region"></a> [primary\_region](#input\_primary\_region) | Primary Region - for ECR, AppConfig, SecretsManager | `string` | `null` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_current_region"></a> [current\_region](#output\_current\_region) | n/a |
| <a name="output_env"></a> [env](#output\_env) | n/a |
| <a name="output_global_key"></a> [global\_key](#output\_global\_key) | n/a |
| <a name="output_main_vpc_private_subnet_cidrs"></a> [main\_vpc\_private\_subnet\_cidrs](#output\_main\_vpc\_private\_subnet\_cidrs) | Networking |
| <a name="output_primary_region"></a> [primary\_region](#output\_primary\_region) | n/a |
<!-- END_TF_DOCS -->