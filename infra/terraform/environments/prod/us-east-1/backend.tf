terraform {
  backend "s3" {
    bucket         = "prod-terraform-backend-450y5"
    key            = "us-east-1/terraform.tfstate" # Use current region here
    region         = "us-east-1"                   # Primery Region (dev) - backend for all regions
    dynamodb_table = "tfstate-lock-prod"
  }
}

# When refactoring terraform config, we may need to update the state manually.
# To do that, we switch to a local backend:
# 1. Comment the S3 backend and uncomment the local backend below
# 2. Run `terraform init -migrate-state` to migrate S3 state into local
# 3. Update terraform state using `terraform state mv <origina-path> <new-path>`
# 4. Ensute `terraform plan` does not re-create any resource
# 5. Run `terraform apply`
# 6. Switch back to S3 backend using 'terraform init -migrate-state` run all state updates, until 'terraform plan' does not create new resources.
# Use local state to run all the changes (e.g. terraform state mv x y) to ensure no resource is recreated.
# Once the state is update so that terraform plan does not recreate exsisting resources,
# Switch back to the s3 backend and rung 'terraform init -migrate-state`
# terraform {
#   backend "local" {
#     path = "terraform-local.tfstate"
#   }
# }
