from flask import Blueprint
from .similarity_controller import similarity_controller

text_mining_controller = Blueprint('text_mining', __name__, url_prefix='/text_mining')

text_mining_controller.register_blueprint(similarity_controller)
