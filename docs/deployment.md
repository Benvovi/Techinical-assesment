# Deployment Guide

## Deployment Strategies

### Rolling Update (Current)

The default deployment strategy uses rolling updates:

```bash
kubectl set image deployment/titanic-api titanic-api=ghcr.io/owner/titanic-api:v1.2.0 -n titanic-prod
kubectl rollout status deployment/titanic-api -n titanic-prod
```

### Blue-Green Deployment (Future)

For zero-downtime deployments, implement blue-green strategy:

1. Deploy new version to "green" environment
2. Test green environment
3. Switch traffic from blue to green
4. Monitor green environment
5. Decommission blue environment

## Deployment Process

### Development Environment

1. **Merge to develop branch**
   ```bash
   git checkout develop
   git merge feature-branch
   git push origin develop
   ```

2. **CI/CD automatically deploys**
   - Tests run
   - Image built and pushed
   - Deployment to dev environment

3. **Verify deployment**
   ```bash
   kubectl get pods -n titanic-dev
   curl http://dev-api.example.com/health
   ```

### Production Environment

1. **Create release branch**
   ```bash
   git checkout main
   git merge develop
   git tag v1.2.0
   git push origin main --tags
   ```

2. **CI/CD pipeline runs**
   - Requires manual approval for production
   - Deploys after approval

3. **Monitor deployment**
   ```bash
   kubectl rollout status deployment/titanic-api -n titanic-prod
   kubectl get pods -n titanic-prod -w
   ```

4. **Verify deployment**
   ```bash
   curl https://api.example.com/health
   # Check metrics and logs
   ```

## Rollback Procedure

### Automatic Rollback

If health checks fail, the deployment automatically rolls back:

```bash
kubectl rollout undo deployment/titanic-api -n titanic-prod
```

### Manual Rollback

1. **Check rollout history**
   ```bash
   kubectl rollout history deployment/titanic-api -n titanic-prod
   ```

2. **Rollback to previous version**
   ```bash
   kubectl rollout undo deployment/titanic-api -n titanic-prod
   ```

3. **Rollback to specific revision**
   ```bash
   kubectl rollout undo deployment/titanic-api --to-revision=2 -n titanic-prod
   ```

## Post-Deployment Verification

1. **Health checks**
   ```bash
   curl https://api.example.com/health
   ```

2. **Check metrics**
   - Prometheus: http://prometheus:9090
   - Grafana: Check dashboard

3. **Check logs**
   ```bash
   kubectl logs -f deployment/titanic-api -n titanic-prod
   ```

4. **Smoke tests**
   ```bash
   # Test API endpoints
   curl https://api.example.com/people
   curl -X POST https://api.example.com/people -d '{"name":"Test"}'
   ```
