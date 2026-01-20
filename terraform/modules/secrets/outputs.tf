output "secret_arn" {
  description = "Secrets Manager secret ARN"
  value       = aws_secretsmanager_secret.database.arn
}

output "secret_id" {
  description = "Secrets Manager secret ID"
  value       = aws_secretsmanager_secret.database.id
}
