# Setup Guide

## Local Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd titanic-api-main
   ```

2. **Start development environment**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

3. **Verify services are running**
   ```bash
   docker-compose -f docker-compose.dev.yml ps
   ```

4. **Check logs**
   ```bash
   docker-compose -f docker-compose.dev.yml logs -f app
   ```

5. **Access the application**
   - API: http://localhost:5000
   - Health: http://localhost:5000/health
   - Metrics: http://localhost:5000/metrics

### Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Kubernetes Deployment

### Prerequisites

- AWS CLI configured
- kubectl installed
- Terraform >= 1.5.0
- kustomize installed

### Steps

1. **Deploy infrastructure with Terraform**
   ```bash
   cd terraform/environments/prod
   terraform init
   terraform plan
   terraform apply
   ```

2. **Configure kubectl**
   ```bash
   aws eks update-kubeconfig --name titanic-api-prod --region us-east-1
   ```

3. **Deploy application**
   ```bash
   kustomize build k8s/overlays/prod | kubectl apply -f -
   ```

4. **Verify deployment**
   ```bash
   kubectl get pods -n titanic-prod
   kubectl get services -n titanic-prod
   ```

5. **Check application logs**
   ```bash
   kubectl logs -f deployment/titanic-api -n titanic-prod
   ```

## CI/CD Pipeline Setup

### GitHub Secrets Configuration

Configure the following secrets in GitHub repository settings:

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `JWT_SECRET_KEY`: JWT secret for authentication
- Database credentials (if needed)

### Triggering Pipeline

The pipeline automatically triggers on:
- Push to `main` branch (deploys to production)
- Push to `develop` branch (deploys to development)
- Pull requests (runs tests only)

## Monitoring Setup

1. **Deploy monitoring stack**
   ```bash
   kubectl apply -f monitoring/k8s/
   ```

2. **Access Grafana**
   ```bash
   kubectl port-forward -n monitoring svc/grafana 3000:3000
   ```
   - URL: http://localhost:3000
   - Default: admin/admin123

3. **Import dashboard**
   - Import `monitoring/grafana/dashboards/titanic-api.json`
