variable "environment" {
  description = "Environment name"
  type        = string
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
}

variable "cluster_oidc_issuer_url" {
  description = "EKS cluster OIDC issuer URL"
  type        = string
  default     = ""
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "titanic-api"
}

variable "service_account_name" {
  description = "Kubernetes service account name"
  type        = string
  default     = "titanic-api-sa"
}

variable "tags" {
  description = "Additional tags"
  type        = map(string)
  default     = {}
}
