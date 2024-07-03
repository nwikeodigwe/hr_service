# HR_SERVICE PLATFORM
<<<<<<< HEAD
# Description
This application is designed to streamline the management of employees across different organizations, providing comprehensive tracking of time, salaries, benefits, and more
# API References
Endpoints                         Method            Parameters                                  Description
/employees/                       GET               -                                           Retrieve all employees
/employees/<id>                   GET               :id                                         Retrieve employee with id
/employees/<id>/salaries          GET               :id                                         Retrieve salary of employee
/employees/<id>/salaries          POST              :id, from_date, to_date                     Create salary for employee
/employees/<id>/timekeeping       GET               :id                                         Retrieve time keeping of employee with given id
/employees/<id>/timekeeping       POST              :id                                         Retrieve time keeping of employee with given id
/employees/     
/employees/<id>/role-pemission    GET               :id                                         Retrieve permission for role of employee
/employees/<id>/org               GET               :id                                         Retrieve organization an employee works for
/employees/<id>/dept              GET               :id                                         Retrieve department of employee with given id
/employees/<id>/salary            GET               :id                                         Retrieve salary of employee
/employees/<id>/timekeeping       GET               :id                                         Retrieve time keeping of employee with given id
/employees/                       POST              name, gender, org_id, role_id               Create new employee
/employees/<id>                   PATCH|PUT         :id, name, organization_id, role_id         Update employee with id
/organizations/                   GET               -                                           Retrieve all organizations
/organizations/<id>               GET               :id                                         Retrieve organization with given id
/organizations/<id>/salaries      GET               :id                                         Retrieve salaries for organization
/organizations/<id>/departments   GET               :id                                         Retrive all departments of an organization
/organizations/<id>/departments   POST              :id, title, description                     Create new department in an organization
/organizations/                   POST              title, description                          Create new organization
/organizations/<id>               PATCH|PUT         :id, title| description |                   Update organization with given id
/oranizations/<id>                DELETE            :id                                         Delete organization with given id
/departments/                     GET                -                                          Retrieve all departments
/departments/<id>                 GET               :id                                         Retrieve department with given id
/departments/<id>                 PATCH|PUT         :id,title, description, organization_id     Update department with id
/departments/<id>                 DELETE            :id                                         Delete department with id
/salaries/                        GET               -                                           Retrieve all  Salaries
/salaries/<id>                    GET               :id                                         Retrieve salary with id
/salaries/<id>                    DELETE            :id                                         delete salary with given id

  
# Data base tables
Employees
id Int Increment Primary Key
firstname String
lastname String
email String
gender String
role ForeignKey
organization ForeignKey
department ForeignKey
created_at Date
updated_at Date
employee_organization
employee_id Int Foreign Key Primary Key
organization_id Foreign Key Primary key
role_id Int


Organization
id Int Increment Primary Key
title
description
departments ForeignKey
created_at
updated_at
employee_department
empoyee_id Int Foreign Key Primary key
department_id Int Foreign Key Primary key


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
Timekeeping
id Int Primary Key
employee_id int foreign key
organization_id int foreign key
time_in date
time_out date



Roles
id Int Increment Primary key
title text
permission ForeignKey
Permissions
id int Increment Primary key
title text
description text
created_at date
Role_permissions
role_id Int Foreign key Primary key
permission_id Int Foreign key Primary key
There are also other possible endpoints that could be added as well as features but for the sake of time and simplicity, I am limiting the scope of this project in the mean time