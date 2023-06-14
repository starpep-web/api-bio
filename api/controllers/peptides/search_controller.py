from flask import Blueprint, request
from api.http.response import ResponseBuilder
from api.http.types import MIME_TYPE_FASTA
from api.http.errors import BadRequestException
from database import db
from lib.bio.fasta import parse_fasta_string, is_single_fasta_valid
from services.alignment.single_query import run_single_query


search_controller = Blueprint('search', __name__, url_prefix='/search')


@search_controller.route('/single-query', methods=['POST'])
def search_single_query():
    content_type = request.headers.get('Content-Type')
    if content_type != MIME_TYPE_FASTA:
        raise BadRequestException(f'Invalid request body type provided, must be {MIME_TYPE_FASTA}')

    fasta_query = request.get_data(as_text=True)
    parsed_fasta = parse_fasta_string(fasta_query)
    if not is_single_fasta_valid(parsed_fasta):
        raise BadRequestException('Request body is not valid FASTA.')

    # TODO: This controller should initialize an async job in another thread. Status should be saved in Redis.
    # TODO: Turn this into a generator to improve performance.
    peptides = db.peptides.get_all_peptides().as_mapped_object()
    result = run_single_query(peptides, parsed_fasta[0])

    return ResponseBuilder().with_data(result).build()
