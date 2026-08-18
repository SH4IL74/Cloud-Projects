resource "aws_dynamodb_table" "vault_records" {
  name         = "vault-records"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}