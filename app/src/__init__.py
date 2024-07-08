import os
from flask import Flask # type: ignore
from flask_migrate import Migrate # type: ignore

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

     # Fetching environment variables
    secret_key = os.getenv('SECRET_KEY', 'dev')
    database_uri = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/serviceplatform')

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=database_uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db

    db.init_app(app)
    migrate = Migrate(app, db)

    
    from .api import employees, organizations, departments, salaries

    app.register_blueprint(employees.bp)
    app.register_blueprint(organizations.bp)
    app.register_blueprint(departments.bp)
    app.register_blueprint(salaries.bp)

    return app
