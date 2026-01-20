terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_secretsmanager_secret" "database" {
  name        = "${var.environment}/titanic-api/database"
  description = "Database credentials for Titanic API"
  
  tags = var.tags
}

resource "aws_secretsmanager_secret_version" "database" {
  secret_id = aws_secretsmanager_secret.database.id
  
  secret_string = jsonencode({
    host     = var.db_host
    port     = 5432
    database = var.db_name
    username = var.db_username
    password = var.db_password
    url      = "postgresql+psycopg2://${var.db_username}:${var.db_password}@${var.db_host}:5432/${var.db_name}"
  })
}
