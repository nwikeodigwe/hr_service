import os
from flask import Flask  # type: ignore
from flask_migrate import Migrate # type: ignore


# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@pg:5432/hrserviceplatform',
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

    from .api import employees
    from .api import organizations
    from .api import departments
    from .api import salaries
    app.register_blueprint(employees.bp)
    app.register_blueprint(organizations.bp)
    app.register_blueprint(departments.bp)
    app.register_blueprint(salaries.bp)

    return app
