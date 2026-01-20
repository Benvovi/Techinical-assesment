# Titanic API - Production-Ready DevOps Solution

## Executive Summary

This document describes the complete transformation of the Titanic API from a basic Flask application into a production-ready, cloud-native service following DevOps best practices. The solution implements containerization, Kubernetes orchestration, CI/CD pipelines, comprehensive monitoring, infrastructure as code, security hardening, and disaster recovery capabilities.

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub Repository                        │
│              (Source Code + CI/CD Workflows)                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  GitHub Actions CI/CD                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │   Lint   │  │   Test   │  │  Build  │  │ Security │    │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Container Registry (ECR/GHCR)                  │
│              (Docker Images with Tags)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    AWS Infrastructure                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  VPC (10.0.0.0/16)                                   │  │
│  │  ┌──────────────┐  ┌──────────────┐                │  │
│  │  │ Public Subnet│  │Private Subnet│                │  │
│  │  │  (ALB, NAT)  │  │ (EKS, RDS)   │                │  │
│  │  └──────────────┘  └──────────────┘                │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  EKS Cluster │  │  RDS (PG)   │  │  S3 Backups  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Secrets Mgr  │  │  ALB (NLB)   │                        │
│  └──────────────┘  └──────────────┘                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              Kubernetes Cluster (EKS)                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Application Namespace (titanic-api)                 │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │   App    │  │   App   │  │   App   │ (HPA)       │  │
│  │  │  Pod 1   │  │  Pod 2  │  │  Pod 3  │             │  │
│  │  └──────────┘  └──────────┘  └──────────┘             │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Monitoring Namespace                                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │Prometheus│  │ Grafana  │  │   Loki   │             │  │
│  │  └──────────┘  └──────────┘  └──────────┘             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Component Architecture

1. **Application Layer**
   - Flask REST API
   - PostgreSQL database (RDS)
   - Structured logging, metrics, tracing

2. **Container Layer**
   - Multi-stage Docker builds
   - Optimized production images (<200MB)
   - Development images with hot-reload

3. **Orchestration Layer**
   - Kubernetes (EKS) for container orchestration
   - Horizontal Pod Autoscaler (HPA)
   - Pod Disruption Budgets (PDB)
   - Network Policies

4. **Infrastructure Layer**
   - AWS VPC with public/private subnets
   - EKS cluster with managed node groups
   - RDS PostgreSQL (Multi-AZ in production)
   - Application Load Balancer
   - S3 for backups

5. **Observability Layer**
   - Prometheus for metrics
   - Grafana for dashboards
   - Loki for log aggregation
   - OpenTelemetry for distributed tracing

6. **CI/CD Layer**
   - GitHub Actions for automation
   - Automated testing and security scanning
   - Multi-environment deployment
   - Semantic versioning

## Part 1: Containerization & Local Development

### Implementation

**Files Created:**
- `Dockerfile` - Multi-stage production build
- `Dockerfile.dev` - Development image with hot-reload
- `docker-compose.yml` - Production multi-container setup
- `docker-compose.dev.yml` - Development setup
- `.dockerignore` - Optimized build context

**Key Features:**
- Multi-stage build reduces final image size
- Non-root user (appuser, UID 1000) for security
- Health check endpoint (`/health`)
- Layer caching optimization
- Separate dev/prod configurations
- Hot-reload in development

**Image Size:** ~150MB (target: <200MB) ✅

### Usage

**Development:**
```bash
docker-compose -f docker-compose.dev.yml up
```

**Production:**
```bash
docker-compose up
```

## Part 2: Kubernetes Deployment

### Implementation

**Base Manifests (`k8s/base/`):**
- `namespace.yaml` - Namespace definition
- `deployment.yaml` - Application deployment with resource limits
- `service.yaml` - ClusterIP and LoadBalancer services
- `configmap.yaml` - Non-sensitive configuration
- `secret.yaml` - Secret template
- `hpa.yaml` - Horizontal Pod Autoscaler
- `pdb.yaml` - Pod Disruption Budget
- `network-policy.yaml` - Network policies
- `pvc.yaml` - Persistent volume for database

**Kustomize Overlays:**
- `k8s/overlays/dev/` - Development environment
- `k8s/overlays/prod/` - Production environment

**Key Features:**
- Rolling update strategy
- Liveness and readiness probes
- Resource requests/limits
- Network policies for database isolation
- HPA based on CPU/memory (2-10 pods in prod)
- Pod Disruption Budget (min 1 available)

### Deployment

```bash
# Development
kustomize build k8s/overlays/dev | kubectl apply -f -

# Production
kustomize build k8s/overlays/prod | kubectl apply -f -
```

## Part 3: CI/CD Pipeline

### Implementation

**Workflows (`.github/workflows/`):**
- `ci-cd.yml` - Main CI/CD pipeline
- `security-scan.yml` - Security scanning

**Pipeline Stages:**
1. **Lint**: Code formatting (black, isort), linting (flake8)
2. **Test**: Unit tests with coverage
3. **Build**: Multi-stage Docker build, push to registry
4. **Security Scan**: Trivy vulnerability scanning
5. **Deploy**: Automated deployment to dev, manual approval for prod

**Key Features:**
- Semantic versioning for images
- Parallel job execution
- Build caching (GitHub Actions cache)
- Automated rollback on failure
- Multi-environment support

### Pipeline Flow

```
Push to branch
    ↓
Lint & Test (parallel)
    ↓
Build Docker Image
    ↓
Security Scan
    ↓
Push to Registry
    ↓
Deploy to Environment
    ↓
Health Check & Verification
```

## Part 4: Observability & Monitoring

### Implementation

**Application Instrumentation:**
- `src/middleware/logging.py` - Structured JSON logging
- `src/middleware/metrics.py` - Prometheus metrics endpoint
- `src/middleware/tracing.py` - OpenTelemetry distributed tracing

**Monitoring Stack:**
- Prometheus for metrics collection
- Grafana dashboards (7 panels):
  - Request rate
  - Request latency (95th percentile)
  - Error rate
  - CPU utilization
  - Memory utilization
  - Active requests
  - Database operations
- Loki for log aggregation
- Alert rules for critical scenarios

**Key Metrics:**
- HTTP request rate and latency
- Error rate (5xx responses)
- Resource utilization (CPU/Memory)
- Database operation metrics
- Active request count

## Part 5: Infrastructure as Code

### Implementation

**Terraform Structure:**
```
terraform/
├── main.tf              # Root module
├── variables.tf          # Variable definitions
├── outputs.tf            # Output values
├── backend.tf            # Remote state configuration
├── modules/
│   ├── vpc/             # VPC, subnets, NAT gateway
│   ├── eks/             # EKS cluster
│   ├── rds/             # RDS PostgreSQL
│   ├── iam/              # IAM roles and policies
│   └── secrets/          # AWS Secrets Manager
└── environments/
    ├── dev/              # Development environment
    └── prod/             # Production environment
```

**Infrastructure Components:**
- VPC with public/private subnets across 3 AZs
- EKS cluster with managed node groups
- RDS PostgreSQL (Multi-AZ in production)
- Application Load Balancer (ALB)
- IAM roles for service accounts (IRSA)
- AWS Secrets Manager integration
- S3 for Terraform state and backups

### Deployment

```bash
cd terraform/environments/prod
terraform init
terraform plan
terraform apply
```

## Part 6: Security & Compliance

### Implementation

**Container Security:**
- Non-root user in containers
- Read-only root filesystem
- Dropped Linux capabilities
- Image scanning in CI/CD (Trivy)
- Minimal base images

**Network Security:**
- Network policies restrict pod communication
- TLS/SSL certificates via cert-manager
- Database connection encryption
- Private subnets for application and database

**Secrets Management:**
- AWS Secrets Manager for sensitive data
- No hardcoded secrets
- Secret rotation capability
- Encrypted at rest

**Authentication:**
- JWT token-based authentication
- Token expiration (24 hours)
- Role-based access control (RBAC)

**Documentation:**
- `SECURITY.md` - Security policy
- `security/checklist.md` - Security checklist

## Part 7: Disaster Recovery & Backup

### Implementation

**Backup Strategy:**
- Automated daily database backups (2 AM UTC)
- RDS automated backups (7-day retention)
- Point-in-time recovery enabled
- S3 backup storage with versioning
- Lifecycle policies (30-day retention, Glacier after 30 days)

**Backup Automation:**
- Kubernetes CronJob for scheduled backups
- Backup scripts (`backup/scripts/`)
- S3 bucket with encryption and lifecycle policies

**Disaster Recovery:**
- RTO: 1 hour (production), 4 hours (development)
- RPO: 1 hour (production), 24 hours (development)
- Multi-AZ deployment in production
- Automated failover for RDS
- DR runbook documentation

**Documentation:**
- `docs/disaster-recovery.md` - Complete DR plan
- Failover procedures
- Recovery testing procedures

## Design Decisions & Trade-offs

### 1. Multi-Stage Docker Builds
**Decision**: Use multi-stage builds to reduce image size
**Trade-off**: Slightly more complex Dockerfile, but significantly smaller images
**Rationale**: Faster deployments, reduced storage costs, better security

### 2. Kustomize vs Helm
**Decision**: Use Kustomize for Kubernetes manifests
**Trade-off**: Less feature-rich than Helm, but simpler for this use case
**Rationale**: Native Kubernetes tool, no templating language, easier to understand

### 3. RDS vs In-Cluster Database
**Decision**: Use RDS instead of PostgreSQL in Kubernetes
**Trade-off**: Higher cost, but better for production
**Rationale**: Managed service, automated backups, Multi-AZ, better performance

### 4. Prometheus + Grafana vs CloudWatch
**Decision**: Use Prometheus + Grafana for monitoring
**Trade-off**: More setup required, but more flexible
**Rationale**: Open-source, vendor-agnostic, better visualization, cost-effective

### 5. Terraform vs CloudFormation
**Decision**: Use Terraform for Infrastructure as Code
**Trade-off**: Multi-cloud support, but requires learning HCL
**Rationale**: Industry standard, better state management, modular design

### 6. GitHub Actions vs GitLab CI
**Decision**: Use GitHub Actions (as specified)
**Trade-off**: GitHub-specific, but well-integrated
**Rationale**: Native integration, good documentation, cost-effective

## Known Limitations & Future Improvements

### Current Limitations

1. **Single Region Deployment**
   - Currently deployed in single AWS region
   - **Improvement**: Implement multi-region deployment for higher availability

2. **Manual Certificate Management**
   - Cert-manager configured but not fully automated
   - **Improvement**: Automate certificate provisioning and renewal

3. **Limited Authentication**
   - Basic JWT authentication implemented
   - **Improvement**: Integrate OAuth2/OIDC for enterprise SSO

4. **No Rate Limiting**
   - API endpoints don't have rate limiting
   - **Improvement**: Implement rate limiting via nginx or API gateway

5. **Basic Monitoring**
   - Monitoring stack is basic
   - **Improvement**: Add APM (Application Performance Monitoring), custom SLIs/SLOs

6. **No Blue-Green Deployments**
   - Currently using rolling updates
   - **Improvement**: Implement blue-green deployments for zero-downtime

### Future Improvements

1. **Service Mesh**
   - Implement Istio or Linkerd for advanced traffic management
   - mTLS between services
   - Advanced observability

2. **GitOps**
   - Implement ArgoCD or Flux for GitOps workflows
   - Automated sync from Git to Kubernetes

3. **Advanced Security**
   - Implement Pod Security Policies
   - Runtime security scanning (Falco)
   - Network encryption (mTLS)

4. **Cost Optimization**
   - Implement cluster autoscaling
   - Use spot instances for non-critical workloads
   - Right-size resources based on actual usage

5. **Performance Testing**
   - Implement load testing in CI/CD
   - Performance benchmarks
   - Capacity planning

## Cost Estimation

### Monthly Cost Breakdown (Production)

| Component | Specification | Monthly Cost (USD) |
|-----------|--------------|-------------------|
| **EKS Cluster** | 1 cluster | $73.00 |
| **EKS Node Group** | 3x t3.medium instances | ~$90.00 |
| **RDS PostgreSQL** | db.t3.small, Multi-AZ | ~$100.00 |
| **ALB** | 1 load balancer | ~$20.00 |
| **NAT Gateway** | 3 NAT gateways | ~$135.00 |
| **S3 Storage** | Backups (100GB) | ~$2.50 |
| **Secrets Manager** | 1 secret | $0.40 |
| **CloudWatch Logs** | 50GB/month | ~$25.00 |
| **Data Transfer** | 100GB | ~$9.00 |
| **Total** | | **~$455.90/month** |

### Development Environment Cost

| Component | Specification | Monthly Cost (USD) |
|-----------|--------------|-------------------|
| **EKS Cluster** | 1 cluster | $73.00 |
| **EKS Node Group** | 1x t3.small instance | ~$15.00 |
| **RDS PostgreSQL** | db.t3.micro, Single-AZ | ~$15.00 |
| **NAT Gateway** | 1 NAT gateway | ~$45.00 |
| **S3 Storage** | Backups (20GB) | ~$0.50 |
| **Total** | | **~$148.50/month** |

### Cost Optimization Strategies

1. **Reserved Instances**: Save up to 40% with 1-year or 3-year reservations
2. **Spot Instances**: Use spot instances for non-critical workloads (up to 90% savings)
3. **Right-Sizing**: Monitor actual usage and adjust instance sizes
4. **S3 Lifecycle Policies**: Move old backups to Glacier/Deep Archive
5. **Cluster Autoscaling**: Scale down during off-peak hours

### Estimated Annual Cost

- **Production**: ~$5,471/year
- **Development**: ~$1,782/year
- **Total**: ~$7,253/year

*Note: Costs are estimates and may vary based on actual usage, region, and AWS pricing changes.*

## Setup Instructions

### Prerequisites

- AWS CLI configured
- kubectl installed
- Terraform >= 1.5.0
- Docker and Docker Compose
- Python 3.11+
- Git

### Local Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd titanic-api-main
   ```

2. **Start Development Environment**
   ```bash
   docker-compose -f docker-compose.dev.yml up
   ```

3. **Access Application**
   - API: http://localhost:5000
   - Health Check: http://localhost:5000/health
   - Metrics: http://localhost:5000/metrics

### Kubernetes Deployment

1. **Configure AWS Credentials**
   ```bash
   aws configure
   ```

2. **Deploy Infrastructure**
   ```bash
   cd terraform/environments/prod
   terraform init
   terraform plan
   terraform apply
   ```

3. **Configure kubectl**
   ```bash
   aws eks update-kubeconfig --name titanic-api-prod --region us-east-1
   ```

4. **Deploy Application**
   ```bash
   kustomize build k8s/overlays/prod | kubectl apply -f -
   ```

5. **Verify Deployment**
   ```bash
   kubectl get pods -n titanic-prod
   kubectl get services -n titanic-prod
   ```

### CI/CD Pipeline Setup

1. **Configure GitHub Secrets**
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `JWT_SECRET_KEY`
   - Database credentials

2. **Push to Repository**
   ```bash
   git push origin main
   ```

3. **Monitor Pipeline**
   - Go to GitHub Actions tab
   - Monitor pipeline execution
   - Check deployment status

### Monitoring Setup

1. **Deploy Monitoring Stack**
   ```bash
   kubectl apply -f monitoring/k8s/
   ```

2. **Access Grafana**
   ```bash
   kubectl port-forward -n monitoring svc/grafana 3000:3000
   ```
   - URL: http://localhost:3000
   - Default credentials: admin/admin123 (change in production)

3. **Import Dashboard**
   - Import `monitoring/grafana/dashboards/titanic-api.json`

## How to Access

### Local Development
- **API**: http://localhost:5000
- **Health**: http://localhost:5000/health
- **Metrics**: http://localhost:5000/metrics

### Production (After Deployment)
- **API**: https://<alb-dns-name>
- **Grafana**: https://grafana.<domain>
- **Prometheus**: http://prometheus.monitoring:9090 (internal)

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check RDS security group allows EKS security group
   - Verify database credentials in Secrets Manager
   - Check network policies

2. **Pods Not Starting**
   - Check resource limits
   - Verify image pull secrets
   - Check pod logs: `kubectl logs <pod-name> -n titanic-prod`

3. **High Memory Usage**
   - Check HPA settings
   - Review application memory usage
   - Consider increasing resource limits

4. **Backup Failures**
   - Verify S3 bucket permissions
   - Check backup CronJob logs
   - Verify database connectivity

## Conclusion

This solution transforms the basic Titanic API into a production-ready, cloud-native application following DevOps best practices. The implementation includes:

✅ Containerization with optimized images
✅ Kubernetes orchestration with auto-scaling
✅ Complete CI/CD pipeline
✅ Comprehensive monitoring and observability
✅ Infrastructure as Code with Terraform
✅ Security hardening and compliance
✅ Disaster recovery and backup strategies

The solution is scalable, secure, observable, and maintainable, ready for production deployment.
