output "appconfig_app_arn" {
  description = "The ARN of the AppConfig app"
  value       = aws_appconfig_application.app.arn
}
