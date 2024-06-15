# HR Platform

# Description

This application is designed to streamline the management of employees across different organizations, providing comprehensive tracking of time, salaries, benefits, and more

# API References

Endpoints Method Parameters Description
/employees/ GET - Retrieve all employees
/employees/<id> GET :id Retrieve employee with id
/employees/<id>/organizations GET :id Retrieve organization an employee works for
/employees/ POST name, gender, organization_id, role_id Create new employee
/employees/<id> PATCH|PUT :id, name, organization_id, role_id Update employee with id
/organizations/ GET - Retrieve all organizations
/organizations/<id> GET :id Retrieve organization with given id
/organizations/<id>/departments GET :id Retrive all departments of an organization
/organizations/ POST user_id,title,description Create new organization
/organizations/<id> PATCH|PUT :id, title| description |Update organization with given id
/oranizations/<id> DELETE :id Delete organization with given id
/departments/ GET - Retrieve all departments
/departments/<id> GET :id Retrieve department with given id
/departments/ POST title, description, organization_id
/departments/<id> PATCH|PUT :id,title, description, organization_id Update comment with id

# Data base tables

Employees
id Int Increment Primary Key
name text
gender
organization_id int foreign key
role_id int foreign key
created_at Date
updated_at Date

Organization
id Int Increment Primary Key
title
description
created_at
updated_at

Departments
id Int Increment Primary Key
organization_id int
title text
description
created_at

Salaries
id Int Increment Primary key
employee_id Int Foreign Key
organization_id Int Foreign key
amount float default(0)
from_data date
to_data date

Benifits
id Int Increment Primary key
employee_id Int Foreign key
organization_id Int
name Text
amount float

Timekeeping
id Int Primary Key
employee_id int foreign key
organization_id int foreign key
from_time date
to_time date

Roles
id Int Increment Primary key
title text

Permissions
id int Increment Primary key
title text
description text
created_at date

Role_permissions
role_id Int Foreign key Primary key
permission_id Int Foreign key Primary key

There are also other possible end points that could be added as well well as features and the purpose of this is to limit the scope of this project in the mean time
