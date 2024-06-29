#!/bin/bash

#echo "Cleaning up existing Terraform initialization..."
#find infra/terraform -type d -name ".terraform" -exec rm -rf {} +
#find infra/terraform -type f -name ".terraform.lock.hcl" -exec rm -f {} +

echo "Initializing and validating main Terraform configuration..."
terraform -chdir=infra/terraform init -backend=false -upgrade
terraform -chdir=infra/terraform validate

echo "Initialize and validate Terraform in each module directory"
for dir in infra/terraform/modules/*; do
  if [ -d "$dir" ]; then
    echo "Initializing and validating Terraform module in $dir..."
    terraform -chdir="$dir" init -backend=false -upgrade
    terraform -chdir="$dir" validate
  fi
done
