<!-- BEGIN_TF_DOCS -->
## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | 5.58.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_appconfig_app"></a> [appconfig\_app](#module\_appconfig\_app) | ../appconfig-app | n/a |

## Resources

| Name | Type |
|------|------|
| [aws_secretsmanager_secret.fake_secret_pair](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret) | resource |
| [aws_secretsmanager_secret.fake_secret_plain](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret) | resource |
| [aws_secretsmanager_secret_version.fake_secret_pair_value](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret_version) | resource |
| [aws_secretsmanager_secret_version.fake_secret_plain_value](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/secretsmanager_secret_version) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_stage"></a> [stage](#input\_stage) | n/a | `string` | `null` | no |
| <a name="input_tags"></a> [tags](#input\_tags) | n/a | `map(string)` | `{}` | no |

## Outputs

No outputs.
<!-- END_TF_DOCS -->