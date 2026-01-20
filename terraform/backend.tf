# Backend configuration for remote state
# This should be configured per environment

terraform {
  backend "s3" {
    # These values should be set via backend config or environment variables
    # bucket         = "titanic-api-terraform-state-${environment}"
    # key            = "terraform.tfstate"
    # region         = "us-east-1"
    # encrypt        = true
    # dynamodb_table = "titanic-api-terraform-locks"
  }
}
