from flask import Blueprint
from api.http.response import ResponseBuilder
from services.database import db


peptide_controller = Blueprint('peptide', __name__, url_prefix='/')


@peptide_controller.route('/', methods=['GET'])
def get_peptides():
    peptides = db.peptides.get_all_peptides().as_mapped_object()
    return ResponseBuilder().with_data(list(peptides)).build()

