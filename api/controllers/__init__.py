from flask import Blueprint
from .health import health_controller
from .peptides import peptides_controller

api = Blueprint('api', __name__)

api.register_blueprint(health_controller)
api.register_blueprint(peptides_controller)
