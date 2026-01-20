"""
OpenTelemetry distributed tracing middleware
"""
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider


def setup_tracing(app, db):
    """
    Configure OpenTelemetry distributed tracing
    
    Args:
        app: Flask application instance
        db: SQLAlchemy database instance
    """
    tracing_enabled = os.getenv('TRACING_ENABLED', 'true').lower() == 'true'
    
    if not tracing_enabled:
        return
    
    # Create resource
    resource = Resource.create({
        "service.name": "titanic-api",
        "service.version": "1.0.0",
    })
    
    # Setup tracer provider
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)
    
    # Add console exporter for development
    if os.getenv('FLASK_ENV') == 'development':
        span_processor = BatchSpanProcessor(ConsoleSpanExporter())
        trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Instrument Flask
    FlaskInstrumentor().instrument_app(app)
    
    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument(
        engine=db.engine,
        tracer_provider=trace.get_tracer_provider()
    )
    
    return tracer
