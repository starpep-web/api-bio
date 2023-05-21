from flask import Blueprint
from .health import health_controller

api = Blueprint('api', __name__)

api.register_blueprint(health_controller)
