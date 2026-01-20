# Disaster Recovery Plan

## Overview

This document outlines the disaster recovery (DR) strategy for the Titanic API application, including Recovery Time Objectives (RTO), Recovery Point Objectives (RPO), and failover procedures.

## Recovery Objectives

### Recovery Time Objective (RTO)
- **Development**: 4 hours
- **Production**: 1 hour

RTO is the maximum acceptable time to restore service after a disaster.

### Recovery Point Objective (RPO)
- **Development**: 24 hours
- **Production**: 1 hour

RPO is the maximum acceptable amount of data loss measured in time.

## Backup Strategy

### Database Backups

#### Automated Backups
- **Frequency**: Daily at 2:00 AM UTC
- **Retention**: 30 days
- **Storage**: S3 with versioning enabled
- **Encryption**: AES-256 encryption at rest
- **Location**: Same region (primary), cross-region replication (optional)

#### RDS Automated Backups
- **Backup Window**: 03:00-04:00 UTC
- **Retention Period**: 7 days
- **Point-in-Time Recovery**: Enabled
- **Multi-AZ**: Enabled in production

#### Manual Backups
- Before major deployments
- Before schema changes
- On-demand via backup scripts

### Configuration Backups

- **Kubernetes Manifests**: Stored in Git repository
- **Terraform State**: Stored in S3 with versioning
- **Secrets**: Stored in AWS Secrets Manager with versioning
- **Monitoring Configs**: Stored in Git repository

### Application Code

- **Source Code**: Git repository (GitHub)
- **Docker Images**: Container registry (ECR/GHCR)
- **Versioning**: Semantic versioning with tags

## Disaster Scenarios

### Scenario 1: Database Failure

**Impact**: Application cannot read/write data

**Recovery Steps**:
1. Identify the failure (RDS status, monitoring alerts)
2. If Multi-AZ: Automatic failover (RTO: ~60 seconds)
3. If Single-AZ or manual failover needed:
   - Restore from latest automated backup
   - Point-in-time recovery if needed
   - Update application connection strings
   - Verify data integrity
   - Resume operations

**RTO**: 15 minutes (Multi-AZ) / 1 hour (Single-AZ restore)
**RPO**: Up to 5 minutes (last transaction)

### Scenario 2: Application Failure

**Impact**: Application pods are down or unhealthy

**Recovery Steps**:
1. Check pod status: `kubectl get pods -n titanic-prod`
2. Check logs: `kubectl logs -n titanic-prod <pod-name>`
3. Restart deployment: `kubectl rollout restart deployment/titanic-api -n titanic-prod`
4. If persistent issues:
   - Rollback to previous version
   - Check resource limits
   - Verify configuration
   - Check database connectivity

**RTO**: 5-15 minutes
**RPO**: None (stateless application)

### Scenario 3: Kubernetes Cluster Failure

**Impact**: Entire cluster is unavailable

**Recovery Steps**:
1. Assess cluster health via AWS Console
2. Attempt cluster recovery
3. If cluster cannot be recovered:
   - Provision new cluster using Terraform
   - Restore application from container registry
   - Restore database from backup
   - Update DNS/load balancer
   - Verify all services

**RTO**: 1-2 hours
**RPO**: Up to 1 hour (last backup)

### Scenario 4: Region Failure

**Impact**: Entire AWS region is unavailable

**Recovery Steps**:
1. Activate disaster recovery region
2. Provision infrastructure using Terraform
3. Restore database from cross-region backup
4. Deploy application to new region
5. Update DNS to point to new region
6. Verify all services

**RTO**: 2-4 hours
**RPO**: Up to 24 hours (last cross-region backup)

### Scenario 5: Data Corruption

**Impact**: Data integrity issues

**Recovery Steps**:
1. Identify corrupted data
2. Stop application to prevent further corruption
3. Restore from point-in-time backup before corruption
4. Verify data integrity
5. Resume operations
6. Investigate root cause

**RTO**: 1-2 hours
**RPO**: Up to 1 hour (point-in-time recovery)

## Failover Procedures

### Automatic Failover

- **RDS Multi-AZ**: Automatic failover in ~60 seconds
- **EKS Node Failure**: Automatic pod rescheduling
- **Load Balancer**: Automatic health check and routing

### Manual Failover

1. **Prepare Secondary Environment**
   - Ensure secondary environment is ready
   - Verify backups are current
   - Test connectivity

2. **Switch Traffic**
   - Update DNS records (TTL: 60 seconds)
   - Update load balancer target groups
   - Verify health checks

3. **Monitor**
   - Check application logs
   - Monitor metrics and alerts
   - Verify database connectivity
   - Check user traffic

4. **Post-Failover**
   - Document incident
   - Investigate root cause
   - Plan remediation
   - Update runbooks if needed

## Multi-AZ Strategy

### Production Environment

- **EKS Cluster**: Nodes across multiple AZs
- **RDS**: Multi-AZ deployment
- **Application**: Pods distributed across AZs
- **Load Balancer**: Cross-AZ routing

### Development Environment

- **EKS Cluster**: Single AZ (cost optimization)
- **RDS**: Single AZ
- **Application**: Single replica

## Backup Testing

### Regular Testing Schedule

- **Weekly**: Verify backup completion
- **Monthly**: Test restore procedure
- **Quarterly**: Full DR drill

### Testing Procedures

1. **Backup Verification**
   ```bash
   aws s3 ls s3://titanic-api-backups/database/
   ```

2. **Restore Test**
   ```bash
   ./backup/scripts/restore-database.sh <backup-file>
   ```

3. **Point-in-Time Recovery Test**
   - Restore to specific timestamp
   - Verify data integrity
   - Test application connectivity

## Monitoring and Alerts

### Backup Monitoring

- **Backup Success**: Alert on backup failure
- **Backup Age**: Alert if backup older than 24 hours
- **S3 Storage**: Alert on storage quota

### Disaster Recovery Alerts

- **RDS Failover**: Alert on Multi-AZ failover
- **Cluster Health**: Alert on cluster issues
- **Application Health**: Alert on pod failures

## Recovery Contacts

- **Primary On-Call**: [Contact Information]
- **Secondary On-Call**: [Contact Information]
- **Database Admin**: [Contact Information]
- **Infrastructure Team**: [Contact Information]

## Post-Recovery Checklist

- [ ] Verify all services are operational
- [ ] Check application logs for errors
- [ ] Verify database connectivity
- [ ] Test critical user flows
- [ ] Monitor metrics for anomalies
- [ ] Document incident and recovery steps
- [ ] Update runbooks based on lessons learned
- [ ] Schedule post-mortem meeting

## Continuous Improvement

- Review and update DR plan quarterly
- Test failover procedures monthly
- Update RTO/RPO based on business requirements
- Document lessons learned from incidents
- Keep backup and restore procedures current
