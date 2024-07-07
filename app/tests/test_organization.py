import sys
import os
import pytest # type: ignore
from flask import Flask # type: ignore

# Add the 'src' directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.api.organizations import bp
from src.models import db

@pytest.fixture
def client():
    # Create and configure a new app instance for each test
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@pg:5432/serviceplatform',  # Update as necessary
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Initialize the database and migration engine
    db.init_app(app)

    # Register the blueprint for organizations
    app.register_blueprint(bp, url_prefix='/organizations')
    
    # Create a test client
    with app.test_client() as client:
        # Set up the database context for each test
        with app.app_context():
            db.create_all()
        
        yield client
        
        # Clean up after each test
        with app.app_context():
            db.drop_all()

def test_create_organization(client):
    # Test POST request to create a new organization
    data = {
        'title': 'PWC',
        'description': 'Your one stop financial tool',
    }
    response = client.post('/organizations', json=data)
    assert response.status_code == 201  # Assuming creation returns 201 Created
    assert 'id' in response.json  # Assuming the response contains the ID of the created organization
    
    # Optionally, assert specific content in the response JSON
    assert response.json['title'] == 'PWC'
    assert response.json['description'] == 'Your one stop financial tool'

def test_update_organization(client):
    # Create an organization to update
    data = {
        'title': 'PWC',
        'description': 'Your one stop financial tool',
    }
    new_organization = client.post('/organizations', json=data)
    assert new_organization.status_code == 201

    organization_id = new_organization.json['id']
    
    # Test PATCH request to update the organization
    update_data = {
        'description': 'Get smarter with our state of the art financial tooling'
    }
    response = client.patch(f'/organizations/{organization_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['description'] == 'Get smarter with our state of the art financial tooling'

def test_retrieve_organization(client):
    # Create an organization to retrieve
    data = {
        'title': 'PWC',
        'description': 'Your one stop financial tool',
    }
    new_organization = client.post('/organizations', json=data)
    assert new_organization.status_code == 201

    organization_id = new_organization.json['id']
    
    # Test GET request to retrieve the organization
    response = client.get(f'/organizations/{organization_id}')
    assert response.status_code == 200
    assert response.json['title'] == 'PWC'

def test_delete_organization(client):
    # Create an organization to delete
    data = {
        'title': 'PWC',
        'description': 'Your one stop financial tool',
    }
    new_organization = client.post('/organizations', json=data)
    assert new_organization.status_code == 201

    organization_id = new_organization.json['id']
    
    # Test DELETE request to delete the organization
    response = client.delete(f'/organizations/{organization_id}')
    assert response.status_code == 200
    assert response.json == True

if __name__ == "__main__":
    pytest.main()
