from flask import Blueprint

bp_api = Blueprint('api', __name__)

from app.api import api_students
