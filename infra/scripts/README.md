# Infrastructure Scripts

## Terraform Setup
[terraform-setup.sh](terraform-setup.sh) scripts creates the resources necessary to manage terraform backend on AWS S3 using Github Actions:
1. S3 bucket - to store bacend state
2. DynamoDB table - to store lock keys
3. Open ID Provider for Github Actions - to allow secured access from Github Actions
4. Github Actions IAM Role with relevant permissions and trust policy

**Configure SSO**
To run the script for each account, one needs to have administrator permissions to dev, staging and prod.
Please ensure to `configure SSO` for each account and name the profile `dev`, `staging`, and `prod` respectively.
Alternatively, edit the `/home/vscode/.aws/config` file to include all three profiles:
```bash
[profile dev]
sso_start_url = __CHANGE_ME__
sso_region = __CHANGE_ME__
sso_account_id = __CHANGE_ME__
sso_role_name = AdministratorAccess
region = __CHANGE_ME__
output = json

[profile staging]
sso_start_url = __CHANGE_ME__
sso_region = __CHANGE_ME__
sso_account_id = __CHANGE_ME__
sso_role_name = AdministratorAccess
region = __CHANGE_ME__
output = json

[profile prod]
sso_start_url = __CHANGE_ME__
sso_region = __CHANGE_ME__
sso_account_id = __CHANGE_ME__
sso_role_name = AdministratorAccess
region = __CHANGE_ME__
output = json
```

**Run the Script**
```bash
terraform-setup.sh <dev|staging|prod>
```