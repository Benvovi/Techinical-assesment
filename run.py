import os

from src.app import create_app

if __name__ == '__main__':
    env_name = os.getenv('FLASK_ENV', default='development')
    app = create_app(env_name)
    
    # Use 127.0.0.1 for local development, 0.0.0.0 only in containers
    host = '0.0.0.0' if os.getenv('FLASK_RUN_HOST') == '0.0.0.0' else '127.0.0.1'
    app.run(host=host)
