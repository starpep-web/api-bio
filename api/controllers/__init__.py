from flask import Blueprint
from .text_mining import text_mining_controller

api = Blueprint('api', __name__)

api.register_blueprint(text_mining_controller)
