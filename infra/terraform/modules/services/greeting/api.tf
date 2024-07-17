
# resource "aws_apigatewayv2_api" "service_api" {
#   name          = "${var.function_name}-api"
#   protocol_type = "HTTP"
# }

# resource "aws_apigatewayv2_stage" "service_stage" {
#   api_id      = aws_apigatewayv2_api.service_api.id
#   name        = var.stage
#   auto_deploy = true
# }

# resource "aws_apigatewayv2_integration" "service_integration" {
#   api_id             = aws_apigatewayv2_api.service_api.id
#   integration_type   = "AWS_PROXY"
#   integration_uri    = aws_lambda_function.service.invoke_arn
#   integration_method = "POST"
# }

# resource "aws_apigatewayv2_route" "hello_name_route" {
#   api_id    = aws_apigatewayv2_api.service_api.id
#   route_key = "GET /hello/{name}"
#   target    = "integrations/${aws_apigatewayv2_integration.service_integration.id}"
# }

# resource "aws_apigatewayv2_route" "hello_route" {
#   api_id    = aws_apigatewayv2_api.service_api.id
#   route_key = "GET /hello"
#   target    = "integrations/${aws_apigatewayv2_integration.service_integration.id}"
# }

# resource "aws_lambda_permission" "api_gw" {
#   statement_id  = "AllowAPIGatewayInvoke"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.service.function_name
#   principal     = "apigateway.amazonaws.com"
#   source_arn    = "${aws_apigatewayv2_api.service_api.execution_arn}/*/*"
# }