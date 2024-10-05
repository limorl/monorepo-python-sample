<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_aws"></a> [aws](#requirement\_aws) | ~> 5.0 |

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_appconfig_deployment_strategy_us_east_1"></a> [appconfig\_deployment\_strategy\_us\_east\_1](#module\_appconfig\_deployment\_strategy\_us\_east\_1) | ../../modules/appconfig | n/a |
| <a name="module_services_us_east_1"></a> [services\_us\_east\_1](#module\_services\_us\_east\_1) | ../../modules/services | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_aws_primary_region"></a> [aws\_primary\_region](#input\_aws\_primary\_region) | Primary Region - for ECR, AppConfig, SecretsManager | `string` | `null` | no |
| <a name="input_stage"></a> [stage](#input\_stage) | General | `string` | `null` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->