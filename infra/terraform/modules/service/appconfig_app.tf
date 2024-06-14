resource "aws_appconfig_application" "app" {
  name        = "service-${var.service_name}"
  description = "AppConfig Application"

  tags = {
    Type = "appconfig_application"
  }
}

resource "aws_appconfig_environment" "appconfig_environment" {
  name           = var.stage
  description    = "AppConfig Environment"
  application_id = aws_appconfig_application.app.id

#   monitor {
#     alarm_arn      = aws_cloudwatch_metric_alarm.example.arn
#     alarm_role_arn = aws_iam_role.example.arn
#   }

  tags = merge(
        var.tags,
        {
            Type = "appconfig_application"
        },
    )
}