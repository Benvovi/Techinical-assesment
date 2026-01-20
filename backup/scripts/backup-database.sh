#!/bin/bash
# Database backup script for RDS PostgreSQL
# This script creates a backup of the database and uploads it to S3

set -e

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-titanic_db}"
DB_USER="${DB_USER:-titanic_user}"
S3_BUCKET="${S3_BUCKET:-titanic-api-backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="titanic_db_backup_${TIMESTAMP}.sql.gz"

# Get database password from AWS Secrets Manager or environment
if [ -z "$DB_PASSWORD" ]; then
    echo "Error: DB_PASSWORD not set"
    exit 1
fi

# Create backup
echo "Creating database backup..."
PGPASSWORD="${DB_PASSWORD}" pg_dump \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    --no-owner \
    --no-acl \
    | gzip > "/tmp/${BACKUP_FILE}"

# Upload to S3
echo "Uploading backup to S3..."
aws s3 cp "/tmp/${BACKUP_FILE}" "s3://${S3_BUCKET}/database/${BACKUP_FILE}"

# Clean up local backup
rm "/tmp/${BACKUP_FILE}"

# Clean up old backups (older than retention period)
echo "Cleaning up old backups..."
aws s3 ls "s3://${S3_BUCKET}/database/" | while read -r line; do
    createDate=$(echo $line | awk {'print $1" "$2'})
    createDate=$(date -d "$createDate" +%s)
    olderThan=$(date -d "${BACKUP_RETENTION_DAYS} days ago" +%s)
    if [[ $createDate -lt $olderThan ]]; then
        fileName=$(echo $line | awk {'print $4'})
        if [[ $fileName != "" ]]; then
            echo "Deleting old backup: $fileName"
            aws s3 rm "s3://${S3_BUCKET}/database/${fileName}"
        fi
    fi
done

echo "Backup completed successfully: ${BACKUP_FILE}"
