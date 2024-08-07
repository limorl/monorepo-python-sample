
resource "aws_secretsmanager_secret" "fake_secret_plain" {
  name                    = "test/fake-secret-plain"
  description             = "Fake secret (plain text) used in integration tests"
  recovery_window_in_days = 0

  tags = merge(
    var.tags,
    {
      Type = "aws_secret_metadata"
    },
  )
}

resource "aws_secretsmanager_secret_version" "fake_secret_plain_value" {
  secret_id     = aws_secretsmanager_secret.fake_secret_plain.id
  secret_string = "fake-secret-val"
}

resource "aws_secretsmanager_secret" "fake_secret_pair" {
  name                    = "test/fake-secret-pair"
  description             = "Fake secret (key-value pair) used in integration tests"
  recovery_window_in_days = 0


  tags = merge(
    var.tags,
    {
      Type = "aws_secret_metadata"
    },
  )
}

resource "aws_secretsmanager_secret_version" "fake_secret_pair_value" {
  secret_id     = aws_secretsmanager_secret.fake_secret_pair.id
  secret_string = "{\"Username\":\"fake-username\",\"Password\":\"fake-password\"}"
}

