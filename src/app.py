from flask import Flask
from .config import app_config
from .models import db
from .views.people import people_api as people
from .middleware.logging import setup_logging
from .middleware.metrics import setup_metrics
from .middleware.tracing import setup_tracing
import os


def create_app(env_name: str) -> Flask:
    """
    Initializes the application registers

    Parameters:
        env_name: the name of the environment to initialize the app with

    Returns:
        The initialized app instance
    """
    app = Flask(__name__)
    app.config.from_object(app_config[env_name])
    
    # Ensure database URI is set (for testing or if env var wasn't set at import time)
    # This is a safety check that only runs if the URI is missing
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    
    db.init_app(app)

    # Setup observability middleware
    setup_logging(app)
    setup_metrics(app)
    setup_tracing(app, db)

    app.register_blueprint(people, url_prefix="/")

    @app.route('/', methods=['GET'])
    def index():
        """
        Root endpoint for populating root route

        Returns:
            Greeting message
        """
        return """
        Welcome to the Titanic API
        """

    @app.route('/health', methods=['GET'])
    def health():
        """
        Health check endpoint for container orchestration

        Returns:
            Health status with database connectivity check
        """
        try:
            # Check database connectivity
            db.session.execute('SELECT 1')
            return {'status': 'healthy', 'database': 'connected'}, 200
        except Exception as e:
            return {'status': 'unhealthy', 'database': 'disconnected', 'error': str(e)}, 503

    return app
