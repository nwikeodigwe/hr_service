from flask import Blueprint, jsonify, abort, request
from ..models import Organization, Employee, Salary, Department, db

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    organizations = Organization.query.all() # ORM performs SELECT query
    result = []
    for o in organizations:
        result.append(o.serialize()) # build list of Posts as dictionaries
    return jsonify(result) # return JSON response6.

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    o = Organization.query.get_or_404(id)
    return jsonify(o.serialize())

@bp.route('/<int:id>/salaries', methods=['GET'])
def salary(id: int):
    o = Organization.query.get_or_404(id)
    salaries = Salary.query.filter_by(organization_id=o.id).all()
    result = []
    for s in salaries:
        result.append(s.serialize())
    return jsonify(result)

@bp.route('/<int:id>/departments', methods=['GET'])
def department(id: int):
    o = Organization.query.get_or_404(id)
    departments = Department.query.filter(Department.organization_id == o.id).all()
    table = []
    for d in departments:
        table.append(d.serialize())
    return jsonify(table)

@bp.route('', methods=['POST'])
def create():
    # req body must contain title and description
    if 'title' not in request.json or 'description' not in request.json:
        return abort(400)
    o = Organization(
        title=request.json['title'],
        description=request.json['description']
    )
    db.session.add(o) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(o.serialize())

@bp.route('/<int:id>/departments', methods=['POST'])
def createdepartment(id: int):
    o = Organization.query.get_or_404(id)
    # req body must contain title and description
    if 'title' not in request.json or 'description' not in request.json:
        return abort(400)
    d = Department(
        organization_id=o.id,
        title=request.json['title'],
        description=request.json['description']
    )
    db.session.add(d) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(d.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    # Find post with id of id
    o = Organization.query.get_or_404(id)
    # user with id of user_id must exist
    
    if request.json.get('title'):
        o.title = request.json.get('title')
    if request.json.get('description'):
        o.description = request.json.get('description')

    db.session.commit() # execute CREATE statement
    return jsonify(o.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    o = Organization.query.get_or_404(id)
    try:
        db.session.delete(o) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)