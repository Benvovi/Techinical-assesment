#!/bin/bash
# Database restore script for RDS PostgreSQL
# This script restores a database from a backup stored in S3

set -e

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-titanic_db}"
DB_USER="${DB_USER:-titanic_user}"
S3_BUCKET="${S3_BUCKET:-titanic-api-backups}"
BACKUP_FILE="${1}"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup-file-name>"
    echo "Available backups:"
    aws s3 ls "s3://${S3_BUCKET}/database/" | awk '{print $4}'
    exit 1
fi

# Get database password
if [ -z "$DB_PASSWORD" ]; then
    echo "Error: DB_PASSWORD not set"
    exit 1
fi

# Download backup from S3
echo "Downloading backup from S3..."
aws s3 cp "s3://${S3_BUCKET}/database/${BACKUP_FILE}" "/tmp/${BACKUP_FILE}"

# Restore database
echo "Restoring database..."
gunzip -c "/tmp/${BACKUP_FILE}" | PGPASSWORD="${DB_PASSWORD}" psql \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}"

# Clean up
rm "/tmp/${BACKUP_FILE}"

echo "Database restored successfully from: ${BACKUP_FILE}"
