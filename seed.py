import random
import datetime
from faker import Faker  # type: ignore
from src.models import Employee, Organization, Department, Role, Salary, Timekeeping, employee_role_table, db
from src import create_app

EMPLOYEE_COUNT = 50
ORGANIZATION_COUNT = 10

def truncate_tables():
    """Delete all rows from database tables"""
    db.session.execute(employee_role_table.delete())
    db.session.query(Salary).delete()
    db.session.query(Timekeeping).delete()
    db.session.query(Employee).delete()
    db.session.query(Department).delete()
    db.session.query(Organization).delete()
    db.session.query(Role).delete()
    db.session.commit()

def main():
    """Main driver function"""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    # Insert Roles
    roles = []
    for _ in range(5):
        role = Role(title=fake.job())
        roles.append(role)
        db.session.add(role)
    
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

    # Insert Departments
    departments = []
    for org in organizations:
        for _ in range(random.randint(1, 5)):  # Each organization can have 1-5 departments
            department = Department(
                description=fake.bs(),
                organization_id=org.id,
                created_at=datetime.datetime.now(datetime.timezone.utc)
            )
            departments.append(department)
            db.session.add(department)

    db.session.commit()

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
        for _ in range(random.randint(1, 5)):
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
                time_in=clock_in,
                time_out=clock_out
            )
            timekeeping.append(time)
            db.session.add(time)

    db.session.commit()

# Run the script
if __name__ == "__main__":
    main()
