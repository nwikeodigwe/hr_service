import random
<<<<<<< HEAD
import datetime
from faker import Faker  # type: ignore
from src.models import Employee, Organization, Department, Role, Salary, Timekeeping, employee_role_table, db
from src import create_app

EMPLOYEE_COUNT = 50
ORGANIZATION_COUNT = 10

def truncate_tables():
    """Delete all rows from database tables in the correct order to avoid foreign key constraint violations."""
    db.session.execute(employee_role_table.delete())
    db.session.query(Salary).delete()
    db.session.query(Employee).delete()
    db.session.query(Department).delete()
    db.session.query(Organization).delete()
    db.session.query(Role).delete()
=======
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
>>>>>>> 23e54bc1dbfe25a099df2bdb0c5c0f44a5fd6778
    db.session.commit()

def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

<<<<<<< HEAD
    # Insert Roles
    roles = []
    for _ in range(5):
        role = Role(title=fake.job())
        roles.append(role)
        db.session.add(role)
    
=======
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

>>>>>>> 23e54bc1dbfe25a099df2bdb0c5c0f44a5fd6778
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

<<<<<<< HEAD
    # Insert Departments
=======
    # Insert Departments and Associate Employees with Organizations
>>>>>>> 23e54bc1dbfe25a099df2bdb0c5c0f44a5fd6778
    departments = []
    for org in organizations:
        for _ in range(random.randint(1, 5)):  # Each organization can have 1-5 departments
            department = Department(
                description=fake.bs(),
<<<<<<< HEAD
                organization_id=org.id,
                created_at=datetime.datetime.now(datetime.timezone.utc)
=======
                organization_id=org.id
>>>>>>> 23e54bc1dbfe25a099df2bdb0c5c0f44a5fd6778
            )
            departments.append(department)
            db.session.add(department)

    db.session.commit()

<<<<<<< HEAD
    # Insert Employees
    employees = []
    for _ in range(EMPLOYEE_COUNT):
        employee = Employee(
            firstname=fake.first_name(),
            lastname=fake.last_name(),
            email=fake.unique.email(),
            gender=random.choice(['M', 'F']),
            birthdate=fake.date_of_birth(),
            role_id=random.choice(roles).id,
            department_id=random.choice(departments).id,
            organization_id=random.choice(organizations).id,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
        )
        employees.append(employee)
        db.session.add(employee)

    db.session.commit()

    # Insert Salaries
    salaries = []
    for employee in employees:
        for _ in range(random.randint(1, 10)):
            from_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            to_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

            # Ensure from_date is before to_date
            if from_date >= to_date:
                from_date, to_date = to_date, from_date

            salary = Salary(
                employee_id=employee.id,
                organization_id=employee.organization_id,
                amount=random.randint(50000, 150000),
                from_date=from_date,
                to_date=to_date
            )
            salaries.append(salary)
            db.session.add(salary)
    db.session.commit()

    # Insert Timekeeping Records
    timekeeping = []
    for employee in employees:
        for _ in range(random.randint(1, 20)):
            clock_in = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            clock_out = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

            # Ensure clock_in is before clock_out
            if clock_in >= clock_out:
                clock_in, clock_out = clock_out, clock_in

            time = Timekeeping(
                employee_id=employee.id,
                organization_id=employee.organization_id,
                department_id=employee.department_id,
                time_in=clock_in,
                time_out=clock_out
            )
            timekeeping.append(time)
            db.session.add(time)
    db.session.commit()

=======
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

>>>>>>> 23e54bc1dbfe25a099df2bdb0c5c0f44a5fd6778
# Run the script
if __name__ == "__main__":
    main()
