from flask import Blueprint
from .status_controller import status_controller

health_controller = Blueprint('health', __name__, url_prefix='/health')

health_controller.register_blueprint(status_controller)
