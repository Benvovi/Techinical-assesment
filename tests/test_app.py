"""
Unit tests for the Titanic API application
"""
import pytest
from src.app import create_app
from src.models import db


@pytest.fixture
def app():
    """Create application for testing"""
    # Set environment variable before creating app
    import os
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
    os.environ['JWT_SECRET_KEY'] = 'test-secret-key'
    
    app = create_app('development')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        # #region agent log
        import json as _json; open('/Users/benjamindurojaiye/Desktop/projects/titanic-api-main/.cursor/debug.log','a').write(_json.dumps({"hypothesisId":"A,C","location":"test_app.py:app_fixture","message":"db config info","data":{"db_uri":app.config.get('SQLALCHEMY_DATABASE_URI'),"dialect":str(db.engine.dialect.name)},"timestamp":__import__('time').time()})+'\n')
        # #endregion
        db.create_all()
        yield app
        db.drop_all()
        # Clean up environment
        os.environ.pop('DATABASE_URL', None)
        os.environ.pop('JWT_SECRET_KEY', None)


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


def test_index_endpoint(client):
    """Test root endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Titanic API' in response.get_data(as_text=True)


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/health')
    assert response.status_code in [200, 503]  # 503 if DB not connected, 200 if healthy


def test_get_people_empty(client):
    """Test getting all people when database is empty"""
    response = client.get('/people')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_add_person(client):
    """Test adding a new person"""
    person_data = {
        "survived": 1,
        "passengerClass": 1,
        "name": "Test Person",
        "sex": "male",
        "age": 30.0,
        "siblingsOrSpousesAboard": 0,
        "parentsOrChildrenAboard": 0,
        "fare": 50.0
    }
    response = client.post('/people', 
                          json=person_data,
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Test Person'
    assert 'uuid' in data


def test_get_person_by_id_not_found(client):
    """Test getting a person that doesn't exist"""
    import uuid
    fake_uuid = str(uuid.uuid4())
    # #region agent log
    import json as _json; open('/Users/benjamindurojaiye/Desktop/projects/titanic-api-main/.cursor/debug.log','a').write(_json.dumps({"hypothesisId":"A,B,C","location":"test_app.py:test_get_person_by_id_not_found","message":"test calling with fake_uuid","data":{"fake_uuid":fake_uuid,"uuid_type":str(type(fake_uuid))},"timestamp":__import__('time').time()})+'\n')
    # #endregion
    response = client.get(f'/people/{fake_uuid}')
    # #region agent log
    import json as _json; open('/Users/benjamindurojaiye/Desktop/projects/titanic-api-main/.cursor/debug.log','a').write(_json.dumps({"hypothesisId":"A,B,C","location":"test_app.py:after_request","message":"response received","data":{"status_code":response.status_code,"response_data":response.get_data(as_text=True)[:200]},"timestamp":__import__('time').time()})+'\n')
    # #endregion
    assert response.status_code == 404
