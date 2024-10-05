# Infrastructure Scripts
Scripts to be used by infrastructure setp.

## Terraform Setup
[terraform-setup.sh](terraform-setup.sh) scripts creates the resources necessary to manage terraform backend on AWS S3 using Github Actions:
1. S3 bucket - to store backend state
2. DynamoDB table - to store lock keys
3. Open ID Provider for Github Actions - to allow secured access from Github Actions
4. Github Actions IAM Role with relevant permissions and trust policy

### Running the script
To run the script for each account (dev, staging and prod), you need to log with Administrator permissions to dev, staging and prod.
Please ensure to run `aws configure SSO` for each account and name the profile `dev`, `staging`, and `prod` respectively.

Alternatively, edit the `~/.aws/config` file to include all three profiles:

>> **Note**: Please do not provide a session name when configuring SSO.

```bash
[profile dev]
sso_start_url = https://**********.awsapps.com/start
sso_region = us-east-1
sso_account_id = __CHANGE_ME__
sso_role_name = AdministratorAccess
region = eu-west-1
output = json

[profile staging]
sso_start_url = https://**********.awsapps.com/start
sso_region = us-east-1
sso_account_id = __CHANGE_ME__
sso_role_name = AdministratorAccess
region = us-east-1
output = json

[profile prod]
sso_start_url = https://**********.awsapps.com/start
sso_region = us-east-1
sso_account_id = __CHANGE_ME__
sso_role_name = AdministratorAccess
region = us-east-1
output = json
```

Then run the script:
```bash
cd infra/scripts
terraform-setup.sh <dev|staging|prod>
```