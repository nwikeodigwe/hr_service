import random
import string
import hashlib
import secrets
import datetime
from faker import Faker  # type: ignore
from services.src.models import Employee, Organization, Department, employee_organization_table, db
from services.src import create_app

EMPLOYEE_COUNT = 50
ORGANIZATION_COUNT = 10
EMPLOYEE_ORGANIZATION_COUNT = 50

assert EMPLOYEE_ORGANIZATION_COUNT <= (EMPLOYEE_COUNT * ORGANIZATION_COUNT)

def random_passhash():
    """Get hashed and salted password of length N | 8 <= N <= 15"""
    raw = ''.join(
        random.choices(
            string.ascii_letters + string.digits + '!@#$%&',  # valid pw characters
            k=random.randint(8, 15)  # length of pw
        )
    )

    salt = secrets.token_hex(16)

    return hashlib.sha512((raw + salt).encode('utf-8')).hexdigest()

def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(employee_organization_table.delete())
    Organization.query.delete()
    Employee.query.delete()
    Department.query.delete()
    db.session.commit()

def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    # Insert Employees
    employees = []
    for _ in range(EMPLOYEE_COUNT):
        employee = Employee(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            email=fake.unique.email(),
            gender=random.choice(['M', 'F']),
            birthdate=fake.date_of_birth(),
        )
        employees.append(employee)
        db.session.add(employee)

    db.session.commit()

    # Insert Organizations
    organizations = []
    for _ in range(ORGANIZATION_COUNT):
        organization = Organization(
            title=fake.company(),
            description=fake.catch_phrase()
        )
        organizations.append(organization)
        db.session.add(organization)

    db.session.commit()

    # Insert Departments and Associate Employees with Organizations
    departments = []
    for org in organizations:
        for _ in range(random.randint(1, 5)):  # Each organization can have 1-5 departments
            department = Department(
                description=fake.bs(),
                organization_id=org.id
            )
            departments.append(department)
            db.session.add(department)

    db.session.commit()

    # Associate Employees with Organizations and Departments
    for _ in range(EMPLOYEE_ORGANIZATION_COUNT):
        employee = random.choice(employees)
        organization = random.choice(organizations)
        department = random.choice(departments)
        db.session.execute(
            employee_organization_table.insert().values(
                employee_id=employee.id,
                organization_id=organization.id,
                role_id=random.randint(1, 5),
                created_at=datetime.datetime.now(datetime.timezone.utc)
            )
        )

    db.session.commit()

# Run the script
if __name__ == "__main__":
    main()
