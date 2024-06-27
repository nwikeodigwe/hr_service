from flask import Blueprint, jsonify, abort, request # type: ignore
from ..models import Employee, Organization, Role, Permission, Salary, Department, Timekeeping, role_permission_table, db



bp = Blueprint('employees', __name__, url_prefix='/employees')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    employees = Employee.query.all() # ORM performs SELECT query
    result = []
    for e in employees:
        result.append(e.serialize()) # build list of users as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    e = Employee.query.get_or_404(id)
    return jsonify(e.serialize())

@bp.route('/<int:id>/role-permission', methods=['GET'])
def role(id: int):
    employee = Employee.query.get_or_404(id)
    
    # Query to get the roles and permissions for the employee
    role_permissions = db.session.query(Role, Permission).join(
        role_permission_table,
        Role.id == role_permission_table.c.role_id
    ).join(
        Permission,
        Permission.id == role_permission_table.c.permission_id
    ).filter(
        Role.id == employee.role_id
    ).all()
    result = []
    for rp in role_permissions:
        result.append(rp.serialize()) # build list of comments as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>/organizations', methods=['GET'])
def organiation(id: int):
    employee = Employee.query.get_or_404(id)
    o = Organization.query.get_or_404(employee.organization_id)
    return jsonify(o.serialize()) # return JSON response6.

@bp.route('/<int:id>/departments', methods=['GET'])
def department(id: int):
    e = Employee.query.get_or_404(id)
    d = Department.query.get_or_404(e.department_id)
    return jsonify(d.serialize()) # return JSON response6.
    
    
@bp.route('/<int:id>/salaries', methods=['GET'])
def salary(id: int):
    e = Employee.query.get_or_404(id)
    salary = Salary.query.filter_by(employee_id=id).all()
    result = []
    for s in salary:
        result.append(s.serialize())
    return jsonify(result)

@bp.route('/<int:id>/timekeeping', methods=['GET'])
def timekeeping(id: int):
    e = Employee.query.get_or_404(id)
    time = Timekeeping.query.filter_by(employee_id=id).all()
    result = []
    for t in time:
        result.append(t.serialize())
    return jsonify(result)

@bp.route('', methods=['POST'])
def create():
    # req body must contain username and password
    if 'firstname' not in request.json or 'lastname' not in request.json or 'email' not in request.json:
        return abort(400)
    # Check if user already exists
    e = Employee.query.filter_by(email=request.json['email']).first()
    if e:
        return abort(400)
    # construct Tweet
    e = Employee(
        firstname=request.json['firstname'],
        lastname=request.json['lastname'],
        email=request.json['email'],
    )
    db.session.add(e) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(e.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):

    #Find the user
    e = Employee.query.get_or_404(id)
    
    if request.json.get('firstname'):
        e.firstname = request.json.get('firstname')
    if request.json.get('lastname'):
        e.lastname = request.json.get('lastname')
    if request.json.get('email'):
        e.email = request.json.get('email')
    if request.json.get('gender'):
        e.gender = request.json.get('gender')
    if request.json.get('birthdate'):
        e.birthdate = request.json.get('birthdate')

    db.session.commit() # execute CREATE statement
    return jsonify(e.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    e = Employee.query.get_or_404(id)
    try:
        db.session.delete(e) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)