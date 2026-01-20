# Titanic API - Production-Ready DevOps Solution

A production-ready Flask REST API for Titanic passenger data, fully containerized and deployed on Kubernetes with comprehensive DevOps practices.

## Quick Start

### Local Development with Docker Compose

```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up

# Access the API
curl http://localhost:5000/health
curl http://localhost:5000/people
```

### Local Development without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/titanic_db

# Run the application
python run.py
```

## Features

- ✅ **Containerization**: Multi-stage Docker builds, optimized images (<200MB)
- ✅ **Kubernetes**: Full K8s deployment with HPA, PDB, Network Policies
- ✅ **CI/CD**: Complete GitHub Actions pipeline with automated testing and deployment
- ✅ **Monitoring**: Prometheus, Grafana, Loki for comprehensive observability
- ✅ **Infrastructure as Code**: Terraform modules for AWS (VPC, EKS, RDS)
- ✅ **Security**: Hardened containers, network policies, secrets management
- ✅ **Disaster Recovery**: Automated backups, DR procedures, multi-AZ deployment

## Documentation

- **[SOLUTION.md](SOLUTION.md)** - Comprehensive solution documentation
- **[docs/setup.md](docs/setup.md)** - Detailed setup instructions
- **[docs/deployment.md](docs/deployment.md)** - Deployment guide
- **[docs/monitoring.md](docs/monitoring.md)** - Monitoring guide
- **[docs/disaster-recovery.md](docs/disaster-recovery.md)** - DR procedures
- **[docs/troubleshooting.md](docs/troubleshooting.md)** - Troubleshooting guide
- **[SECURITY.md](SECURITY.md)** - Security policy and practices

## Architecture

- **Application**: Flask REST API with PostgreSQL
- **Containerization**: Docker with multi-stage builds
- **Orchestration**: Kubernetes (EKS) with auto-scaling
- **Infrastructure**: AWS (VPC, EKS, RDS, ALB, S3)
- **Monitoring**: Prometheus + Grafana + Loki
- **CI/CD**: GitHub Actions

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /metrics` - Prometheus metrics
- `GET /people` - Get all people
- `GET /people/<uuid>` - Get person by UUID
- `POST /people` - Create new person
- `PUT /people/<uuid>` - Update person
- `DELETE /people/<uuid>` - Delete person

## Development

### Running Tests

```bash
pytest
pytest --cov=src --cov-report=html
```

### Building Docker Image

```bash
docker build -t titanic-api:latest .
```

## Deployment

See [docs/deployment.md](docs/deployment.md) for detailed deployment instructions.

### Quick Deploy to Kubernetes

```bash
# Deploy infrastructure
cd terraform/environments/prod
terraform apply

# Deploy application
kustomize build k8s/overlays/prod | kubectl apply -f -
```

## License

[Add your license here]

## Contributing

[Add contributing guidelines here]
