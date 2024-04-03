module "hello_world_lambda" {
  source = "./modules/lambda"

  function_name = "hello_world"
  s3_bucket     = "your_bucket_name"
  s3_key        = "hello_world.zip"
  handler       = "index.handler"
  runtime       = "nodejs14.x"
}

module "hello_world_lambda" {
  source             = "./modules/lambda"
  function_name      = "hello_world"
  s3_key             = "hello_world.zip"
  handler            = "index.handler"
  runtime            = "nodejs14.x"
  environment        = "Dev"
  subnet_ids         = ["subnet-xxxxxx", "subnet-yyyyyy"]
  security_group_ids = ["sg-xxxxxx"]
}


module "greeting_lambda" {
  source = "./modules/lambda"

  function_name = "greeting"
  s3_bucket     = "your_bucket_name"
  s3_key        = "greeting.zip"
  handler       = "index.handler"
  runtime       = "nodejs14.x"
}
