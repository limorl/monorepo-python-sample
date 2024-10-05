output "appconfig_test_app" {
  value = module.appconfig_test_app.appconfig_app_arn
}

output "test_secrets" {
  value = {
    fake_secret_plain_name  = local.fake_secret_plain_name
    fake_secret_plain_value = local.fake_secret_plain_value

    fake_secret_pair_name  = local.fake_secret_pair_name
    fake_secret_pair_value = local.fake_secret_pair_value
  }
}
