from flask import Blueprint, jsonify, abort, request # type: ignore
from ..models import Department, db

bp = Blueprint('departments', __name__, url_prefix='/departments')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    departments = Department.query.all() # ORM performs SELECT query
    result = [d.serialize() for d in departments] # build list of departments as dictionaries
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    d = Department.query.get_or_404(id)
    return jsonify(d.serialize())

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    # department with id must exist
    d = Department.query.get_or_404(id)

    if request.json.get('title'):
        d.title = request.json.get('title')
    if request.json.get('description'):
        d.description = request.json.get('description')
    db.session.commit() # execute statement
    return jsonify(d.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    d = Department.query.get_or_404(id)
    try:
        db.session.delete(d) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

