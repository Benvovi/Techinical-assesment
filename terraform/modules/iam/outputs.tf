output "cluster_role_arn" {
  description = "EKS cluster IAM role ARN"
  value       = aws_iam_role.cluster.arn
}

output "node_role_arn" {
  description = "EKS node group IAM role ARN"
  value       = aws_iam_role.node.arn
}

output "service_account_role_arn" {
  description = "Service account IAM role ARN"
  value       = aws_iam_role.service_account.arn
}
