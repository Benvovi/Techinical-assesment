# Troubleshooting Guide

## Common Issues

### Database Connection Issues

**Symptoms:**
- Application cannot connect to database
- Health check fails
- 503 errors

**Solutions:**
1. Check RDS security group allows EKS security group
2. Verify database credentials in Secrets Manager
3. Check network policies
4. Verify database endpoint is correct

```bash
# Check database connectivity
kubectl exec -it <pod-name> -n titanic-prod -- psql -h <db-endpoint> -U <user> -d <database>
```

### Pod Not Starting

**Symptoms:**
- Pods in Pending or CrashLoopBackOff state

**Solutions:**
1. Check resource limits
   ```bash
   kubectl describe pod <pod-name> -n titanic-prod
   ```

2. Check image pull secrets
   ```bash
   kubectl get secrets -n titanic-prod
   ```

3. Check pod logs
   ```bash
   kubectl logs <pod-name> -n titanic-prod
   ```

4. Check events
   ```bash
   kubectl get events -n titanic-prod --sort-by='.lastTimestamp'
   ```

### High Memory Usage

**Symptoms:**
- Pods being OOMKilled
- High memory metrics

**Solutions:**
1. Check HPA settings
   ```bash
   kubectl get hpa -n titanic-prod
   ```

2. Review application memory usage
3. Increase resource limits if needed
4. Optimize application code

### Backup Failures

**Symptoms:**
- Backup CronJob failing
- No backups in S3

**Solutions:**
1. Check CronJob logs
   ```bash
   kubectl logs job/<backup-job-name> -n titanic-api
   ```

2. Verify S3 bucket permissions
3. Check database connectivity
4. Verify backup script permissions

### CI/CD Pipeline Failures

**Symptoms:**
- Pipeline failing at build or deploy stage

**Solutions:**
1. Check GitHub Actions logs
2. Verify AWS credentials
3. Check Docker image build logs
4. Verify Kubernetes cluster access

### Monitoring Not Working

**Symptoms:**
- No metrics in Prometheus
- Grafana dashboards empty

**Solutions:**
1. Check Prometheus targets
   ```bash
   kubectl port-forward -n monitoring svc/prometheus 9090:9090
   # Visit http://localhost:9090/targets
   ```

2. Verify ServiceMonitor
   ```bash
   kubectl get servicemonitor -n monitoring
   ```

3. Check Prometheus configuration
4. Verify pod annotations for scraping

## Debugging Commands

### Kubernetes

```bash
# Get pod status
kubectl get pods -n titanic-prod

# Describe pod
kubectl describe pod <pod-name> -n titanic-prod

# Get logs
kubectl logs -f <pod-name> -n titanic-prod

# Execute command in pod
kubectl exec -it <pod-name> -n titanic-prod -- /bin/sh

# Get events
kubectl get events -n titanic-prod --sort-by='.lastTimestamp'
```

### Application

```bash
# Health check
curl http://localhost:5000/health

# Metrics
curl http://localhost:5000/metrics

# Test endpoint
curl http://localhost:5000/people
```

### Database

```bash
# Connect to database
psql -h <endpoint> -U <user> -d <database>

# Check connections
SELECT count(*) FROM pg_stat_activity;

# Check database size
SELECT pg_size_pretty(pg_database_size('<database>'));
```

## Getting Help

1. Check logs first
2. Review documentation
3. Check GitHub Issues
4. Contact team
