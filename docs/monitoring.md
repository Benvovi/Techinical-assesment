# Monitoring Guide

## Metrics

### Application Metrics

Available at `/metrics` endpoint:

- `http_requests_total`: Total HTTP requests
- `http_request_duration_seconds`: Request latency
- `http_requests_active`: Active requests
- `database_operations_total`: Database operations
- `database_operation_duration_seconds`: Database operation latency

### Infrastructure Metrics

- CPU utilization
- Memory utilization
- Network I/O
- Disk I/O
- Pod status

## Dashboards

### Grafana Dashboard

Access Grafana:
```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

Dashboard URL: http://localhost:3000

**Panels:**
1. Request Rate
2. Request Latency (95th percentile)
3. Error Rate
4. CPU Utilization
5. Memory Utilization
6. Active Requests
7. Database Operations

## Alerts

### Alert Rules

Configured in `monitoring/prometheus/rules.yaml`:

- **HighErrorRate**: Error rate > 5% for 5 minutes
- **HighLatency**: 95th percentile latency > 1 second
- **PodCrashLooping**: Pod restarting frequently
- **HighCPUUsage**: CPU usage > 80%
- **HighMemoryUsage**: Memory usage > 90%
- **DatabaseConnectionFailure**: Cannot connect to database

### Alerting

Alerts are sent to Alertmanager and can be configured to:
- Send to Slack
- Send email
- Create PagerDuty incidents

## Logging

### Structured Logs

Application logs are in JSON format:
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "level": "INFO",
  "message": "Request completed",
  "method": "GET",
  "path": "/people",
  "status_code": 200,
  "duration_ms": 45.2
}
```

### Log Aggregation

Logs are collected by Loki and can be queried in Grafana.

### Viewing Logs

```bash
# Kubernetes logs
kubectl logs -f deployment/titanic-api -n titanic-prod

# Loki logs (via Grafana)
# Use Grafana Explore to query Loki
```

## Tracing

### OpenTelemetry

Distributed tracing is implemented using OpenTelemetry:

- Traces requests across services
- Shows request flow
- Identifies bottlenecks

### Viewing Traces

Traces can be viewed in:
- Jaeger (if configured)
- Grafana Tempo (if configured)
- CloudWatch X-Ray (AWS)

## Troubleshooting

### High Error Rate

1. Check application logs
2. Check database connectivity
3. Review recent deployments
4. Check resource limits

### High Latency

1. Check database query performance
2. Review resource utilization
3. Check network policies
4. Review application code

### Pod Failures

1. Check pod logs
2. Check resource limits
3. Verify image pull
4. Check health probes
