import datetime
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

# Association tables
role_permission_table = db.Table(
    'role_permission',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'))
)

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(128), nullable=False)
    lastname = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    gender = db.Column(db.String(1), nullable=True)
    birthdate = db.Column(db.Date, nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    salary = db.relationship('Salary', backref='employee', cascade="all, delete")
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now(datetime.UTC), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'gender': self.gender,
            'birthdate': self.birthdate.isoformat() if self.birthdate else None,
            'role_id': self.role_id,
            'department_id': self.department_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, default='Untitled')
    description = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), onupdate=datetime.datetime.now(datetime.UTC), nullable=False)
    departments = db.relationship('Department', backref='organization', cascade="all, delete")

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False, default='Untitled')
    description = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'organization_id': self.organization_id,
        }

class Salary(db.Model):
    __tablename__ = 'salaries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    amount = db.Column(db.Float(), nullable=False, default=0.0)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(datetime.UTC), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'organization_id': self.organization_id,
            'amount': self.amount,
            'from_date': self.from_date.isoformat(),
            'to_date': self.to_date.isoformat()
        }

class Timekeeping(db.Model):
    __tablename__ = 'timekeeping'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    time_in = db.Column(db.DateTime, nullable=False)
    time_out = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'organization_id': self.organization_id,
            'department_id': self.department_id,
            'time_in': self.time_in.isoformat(),
            'time_out': self.time_out.isoformat()
        }

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(280), nullable=True)
    permissions = db.relationship('Permission', secondary=role_permission_table, backref=db.backref('roles', lazy=True))

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description
        }

class Permission(db.Model):
    __tablename__ = 'permissions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(280), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
        }
