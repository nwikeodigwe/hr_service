import sys
import os
import pytest # type: ignore
from flask import Flask # type: ignore

# Add the 'src' directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.api.employees import bp
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

    # Register the blueprint for employees
    app.register_blueprint(bp, url_prefix='/employees')
    
    # Create a test client
    with app.test_client() as client:
        # Set up the database context for each test
        with app.app_context():
            db.create_all()
        
        yield client
        
        # Clean up after each test
        with app.app_context():
            db.drop_all()

def test_create_employee(client):
    # Test POST request to create a new employee
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'johndoe@email.com'
    }
    response = client.post('/employees', json=data)
    assert response.status_code == 201  # Assuming creation returns 201 Created
    assert 'id' in response.json  # Assuming the response contains the ID of the created employee
    
    # Optionally, assert specific content in the response JSON
    assert response.json['firstname'] == 'John'
    assert response.json['lastname'] == 'Doe'
    assert response.json['email'] == 'johndoe@email.com'

def test_update_employee(client):
    # Create an employee to update
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'johndoe@email.com'
    }
    new_employee = client.post('/employees', json=data)
    assert new_employee.status_code == 201

    employee_id = new_employee.json['id']
    
    # Test PATCH request to update the employee
    update_data = {
        'firstname': 'Jon'
    }
    response = client.patch(f'/employees/{employee_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['firstname'] == 'Jon'

def test_retrieve_employee(client):
    # Create an employee to retrieve
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'johndoe@email.com'
    }
    new_employee = client.post('/employees', json=data)
    assert new_employee.status_code == 201

    employee_id = new_employee.json['id']
    
    # Test GET request to retrieve the employee
    response = client.get(f'/employees/{employee_id}')
    assert response.status_code == 200
    assert response.json['firstname'] == 'John'

def test_delete_employee(client):
    # Create an employee to delete
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'johndoe@email.com'
    }
    new_employee = client.post('/employees', json=data)
    assert new_employee.status_code == 201

    employee_id = new_employee.json['id']
    
    # Test DELETE request to delete the employee
    response = client.delete(f'/employees/{employee_id}')
    assert response.status_code == 200
    assert response.json == True

if __name__ == "__main__":
    pytest.main()
