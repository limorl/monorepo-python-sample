locals {
  site_configurations_table_name = "site-configurations-${var.env}"
}

module "site_configurations_table" {
  source = "../aws-dynamodb-hash-table"

  env            = var.env
  table_name     = local.site_configurations_table_name
  billing_mode   = "PROVISIONED" # Our scale is predictable and consistent
  read_capacity  = 6             # 1000 reads every 3 minutes = 5.55 reads very second
  write_capacity = 1             # Writes are very rare
  hash_key       = "site_id"


  tags = merge(
    var.tags,
    {
      Data = local.site_configurations_table_name
    }
  )
}
