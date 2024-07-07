from flask import Blueprint, jsonify, abort, request # type: ignore
from ..models import Salary, db

bp = Blueprint('salaries', __name__, url_prefix='/salaries')

@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    salaries = Salary.query.all() # ORM performs SELECT query
    result = [s.serialize() for s in salaries] # build list of departments as dictionaries
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    s = Salary.query.get_or_404(id)
    return jsonify(s.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    d = Salary.query.get_or_404(id)
    try:
        db.session.delete(d) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)

