from flask import Blueprint
from .peptide_controller import peptide_controller
from .search_controller import search_controller

peptides_controller = Blueprint('peptides', __name__, url_prefix='/peptides')

peptides_controller.register_blueprint(peptide_controller)
peptides_controller.register_blueprint(search_controller)
