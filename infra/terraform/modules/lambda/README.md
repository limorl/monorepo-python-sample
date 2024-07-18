<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.58.0 |
| <a name="provider_time"></a> [time](#provider\_time) | 0.12.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_iam_role.lambda_role](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role) | resource |
| [aws_iam_role_policy.lambda_appconfig_secretsmanager_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy.lambda_ecr_policy](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy) | resource |
| [aws_iam_role_policy_attachment.lambda_basic](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/iam_role_policy_attachment) | resource |
| [aws_lambda_function.function](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/lambda_function) | resource |
| [aws_iam_policy_document.ecr_policy_document](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/iam_policy_document) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_docker_tag"></a> [docker\_tag](#input\_docker\_tag) | The tag of the Docker image to use | `string` | `"latest"` | no |
| <a name="input_ecr_repository_arn"></a> [ecr\_repository\_arn](#input\_ecr\_repository\_arn) | The ARN of the ECR repository | `string` | n/a | yes |
| <a name="input_ecr_repository_policy"></a> [ecr\_repository\_policy](#input\_ecr\_repository\_policy) | The ECR repository policy | `any` | `null` | no |
| <a name="input_ecr_repository_url"></a> [ecr\_repository\_url](#input\_ecr\_repository\_url) | The URL of the ECR repository | `string` | n/a | yes |
| <a name="input_function_name"></a> [function\_name](#input\_function\_name) | n/a | `string` | `null` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(string)` | `{}` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_lambda_role_arn"></a> [lambda\_role\_arn](#output\_lambda\_role\_arn) | The ARN of the Lambda execution role |
<!-- END_TF_DOCS -->