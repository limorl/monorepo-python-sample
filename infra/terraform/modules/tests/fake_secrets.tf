resource "aws_secretsmanager_secret" "fake_secret_plain" {
  name        = "test/fake-secret-plain-${random_id.suffix.hex}"
  description = "Fake secret used in integration tests"

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
  name        = "test/fake-secret-pair-${random_id.suffix.hex}"
  description = "Fake secret used in integration tests"

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

