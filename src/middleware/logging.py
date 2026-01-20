"""
Structured JSON logging middleware
"""
import json
import logging
import os
from datetime import datetime
from pythonjsonlogger import jsonlogger
from flask import request, g


def setup_logging(app):
    """
    Configure structured JSON logging for the application
    
    Args:
        app: Flask application instance
    """
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    
    # Create custom formatter
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s',
        timestamp=True
    )
    
    # Configure root logger
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))
    logger.addHandler(handler)
    
    # Set Flask logger
    app.logger.setLevel(getattr(logging, log_level))
    app.logger.addHandler(handler)
    
    @app.before_request
    def log_request_info():
        """Log request information"""
        g.start_time = datetime.utcnow()
        app.logger.info('Request started', extra={
            'method': request.method,
            'path': request.path,
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
        })
    
    @app.after_request
    def log_response_info(response):
        """Log response information"""
        duration = (datetime.utcnow() - g.start_time).total_seconds() * 1000
        
        app.logger.info('Request completed', extra={
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': round(duration, 2),
            'response_size': len(response.get_data()),
        })
        
        return response
    
    @app.errorhandler(Exception)
    def log_exception(error):
        """Log exceptions"""
        app.logger.error('Unhandled exception', extra={
            'error_type': type(error).__name__,
            'error_message': str(error),
            'path': request.path,
            'method': request.method,
        }, exc_info=True)
        raise error
