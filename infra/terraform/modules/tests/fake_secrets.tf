locals {
  fake_secret_plain_name  = "test/fake-secret-plain"
  fake_secret_plain_value = "fake-secret-val"

  fake_secret_pair_name  = "test/fake-secret-pair"
  fake_secret_pair_value = "{\"Username\":\"fake-username\",\"Password\":\"fake-password\"}"
}

resource "aws_secretsmanager_secret" "fake_secret_plain" {
  name                    = local.fake_secret_plain_name
  description             = "Fake secret used in integration tests"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "fake_secret_plain_value" {
  secret_id     = aws_secretsmanager_secret.fake_secret_plain.id
  secret_string = local.fake_secret_plain_value
}

resource "aws_secretsmanager_secret" "fake_secret_pair" {
  name                    = local.fake_secret_pair_name
  description             = "Fake secret used in integration tests"
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "fake_secret_pair_value" {
  secret_id     = aws_secretsmanager_secret.fake_secret_pair.id
  secret_string = local.fake_secret_pair_value
}

