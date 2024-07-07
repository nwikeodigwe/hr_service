import random
import datetime
from faker import Faker # type: ignore
from src.models import Employee, Organization, Department, Role, Permission, Salary, Timekeeping, role_permission_table, db
from src import create_app

EMPLOYEE_COUNT = 50
ORGANIZATION_COUNT = 10

def truncate_tables():
    """Delete all rows from database tables."""
    db.session.query(Salary).delete()
    db.session.query(Timekeeping).delete()
    db.session.query(Employee).delete()
    db.session.query(Department).delete()
    db.session.query(Organization).delete()
    db.session.query(Role).delete()
    db.session.query(Permission).delete()
    db.session.query(role_permission_table).delete()
    db.session.commit()

def main():
    """Main function to populate database with synthetic data."""
    app = create_app()
    app.app_context().push()
    truncate_tables()
    fake = Faker()

    # Insert Roles
    roles = []
    for _ in range(5):
        role = Role(title=fake.job(), description=fake.catch_phrase())
        db.session.add(role)
        roles.append(role)
    
    db.session.commit()

    # Insert Permissions
    permissions = []
    for _ in range(10):
        permission = Permission(title=fake.word(), description=fake.sentence())
        db.session.add(permission)
        permissions.append(permission)
    
    db.session.commit()

    # Assign Permissions to Roles
    for role in roles:
        assigned_permissions = random.sample(permissions, k=random.randint(1, len(permissions)))
        role.permissions.extend(assigned_permissions)
    
    db.session.commit()

    # Insert Organizations
    organizations = []
    for _ in range(ORGANIZATION_COUNT):
        organization = Organization(
            title=fake.company(),
            description=fake.catch_phrase()
        )
        db.session.add(organization)
        organizations.append(organization)
    
    db.session.commit()

    # Insert Departments
    departments = []
    for org in organizations:
        for _ in range(random.randint(1, 5)):
            department = Department(
                title=fake.job(),
                description=fake.bs(),
                organization_id=org.id
            )
            db.session.add(department)
            departments.append(department)
    
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
            organization_id=random.choice(organizations).id,
            department_id=random.choice(departments).id if departments else None,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )
        db.session.add(employee)
        employees.append(employee)
    
    db.session.commit()

    # Insert Salaries
    salaries = []
    for employee in employees:
        for _ in range(random.randint(1, 5)):
            from_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            to_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            if from_date >= to_date:
                from_date, to_date = to_date, from_date

            salary = Salary(
                employee_id=employee.id,
                organization_id=employee.organization_id,
                amount=random.randint(50000, 150000),
                from_date=from_date.date(),
                to_date=to_date.date(),
                created_at=datetime.datetime.utcnow()
            )
            db.session.add(salary)
            salaries.append(salary)
    
    db.session.commit()

    # Insert Timekeeping Records
    timekeeping_records = []
    for employee in employees:
        for _ in range(random.randint(1, 20)):
            time_in = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            time_out = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
            if time_in >= time_out:
                time_in, time_out = time_out, time_in

            timekeeping = Timekeeping(
                employee_id=employee.id,
                organization_id=employee.organization_id,
                department_id=employee.department_id if employee.department_id else random.choice(departments).id,
                time_in=time_in,
                time_out=time_out
            )
            db.session.add(timekeeping)
            timekeeping_records.append(timekeeping)
    
    db.session.commit()

if __name__ == "__main__":
    main()
