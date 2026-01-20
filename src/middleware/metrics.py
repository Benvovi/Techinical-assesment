"""
Prometheus metrics middleware
"""
import os
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from flask import request, Response


# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests'
)

DATABASE_OPERATIONS = Counter(
    'database_operations_total',
    'Total database operations',
    ['operation', 'table']
)

DATABASE_DURATION = Histogram(
    'database_operation_duration_seconds',
    'Database operation duration in seconds',
    ['operation', 'table']
)


def setup_metrics(app):
    """
    Configure Prometheus metrics for the application
    
    Args:
        app: Flask application instance
    """
    metrics_enabled = os.getenv('METRICS_ENABLED', 'true').lower() == 'true'
    
    if not metrics_enabled:
        return
    
    @app.before_request
    def before_request():
        """Track active requests"""
        ACTIVE_REQUESTS.inc()
    
    @app.after_request
    def after_request(response):
        """Record request metrics"""
        ACTIVE_REQUESTS.dec()
        
        # Record request count
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.endpoint or request.path,
            status=response.status_code
        ).inc()
        
        # Record request duration
        if hasattr(request, '_start_time'):
            duration = (request._start_time - request._start_time).total_seconds()
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.endpoint or request.path
            ).observe(duration)
        
        return response
    
    @app.route('/metrics', methods=['GET'])
    def metrics():
        """
        Prometheus metrics endpoint
        
        Returns:
            Prometheus metrics in text format
        """
        return Response(
            generate_latest(),
            mimetype=CONTENT_TYPE_LATEST
        )
