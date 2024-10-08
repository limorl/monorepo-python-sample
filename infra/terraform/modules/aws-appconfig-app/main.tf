resource "aws_appconfig_application" "app" {
  name        = var.app_name
  description = "AppConfig Application"

  tags = var.tags
}

resource "aws_appconfig_environment" "appconfig_environment" {
  name           = var.env_name
  description    = "AppConfig Environment"
  application_id = aws_appconfig_application.app.id

  tags = var.tags
}
