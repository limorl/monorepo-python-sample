<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

No providers.

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_appconfig_app"></a> [appconfig\_app](#module\_appconfig\_app) | ../appconfig-app | n/a |
| <a name="module_ecr_repository"></a> [ecr\_repository](#module\_ecr\_repository) | ../ecr-repository | n/a |
| <a name="module_lambda_function"></a> [lambda\_function](#module\_lambda\_function) | ../lambda | n/a |

## Resources

No resources.

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_service_name"></a> [service\_name](#input\_service\_name) | n/a | `string` | `null` | no |
| <a name="input_stage"></a> [stage](#input\_stage) | n/a | `string` | `null` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_role_arn"></a> [lambda\_role\_arn](#output\_lambda\_role\_arn) | The ARN of the Lambda IAM role |
<!-- END_TF_DOCS -->