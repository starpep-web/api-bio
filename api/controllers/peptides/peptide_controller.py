from flask import Blueprint
from api.http.response import ResponseBuilder
from database import db


peptide_controller = Blueprint('peptide', __name__, url_prefix='/')


@peptide_controller.route('/', methods=['GET'])
def get_peptides():
    peptides = db.peptides.get_all_peptides().as_mapped_object()
    return ResponseBuilder().with_data(peptides).build()


@peptide_controller.route('/<sequence>', methods=['GET'])
def get_peptide_by_sequence(sequence: str):
    peptides = db.peptides.get_full_peptide(sequence).as_mapped_object()
    return ResponseBuilder().with_data(peptides).build()
