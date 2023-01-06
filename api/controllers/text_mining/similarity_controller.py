from flask import request, Blueprint
from http_constants.status import HttpStatus
from ...http.response import ResponseBuilder
from ...http.errors import MissingParameterException
from tools.text_mining.similarity import TfidfSimilarity, FastTextSimilarity
from data.graph_db import db_service


similarity_controller = Blueprint('similarity', __name__, url_prefix='/similarity')


@similarity_controller.route('/tfidf', methods=['GET'])
def get_tfidf_similarity():
    query = request.args.get('q', type=str)
    if not query:
        raise MissingParameterException('q parameter is required.')

    limit = request.args.get('limit', type=int)
    treshold = request.args.get('treshold', type=float)

    # Should trained models be cached instead of training on-request?
    # Or maybe models should be loaded on-request to avoid keeping them in memory?
    peptides = db_service.fetch_peptides().as_np().flatten()
    model = TfidfSimilarity()
    model.train(peptides)
    result = model.compare_query(query, limit=limit, treshold=treshold)  # No max limit set, may slow down server if limit is not provided.

    return ResponseBuilder().with_status_code(int(HttpStatus.OK)).with_data(result).build()


@similarity_controller.route('/fasttext', methods=['GET'])
def get_fasttext_similarity():
    query = request.args.get('q', type=str)
    if not query:
        raise MissingParameterException('q parameter is required.')

    limit = request.args.get('limit', type=int)
    treshold = request.args.get('treshold', type=float)

    model = FastTextSimilarity()
    model.load()
    result = model.compare_query(query, limit=limit, treshold=treshold)  # Default limit is 10, should we check for an actual max value to avoid slowing down the server?

    return ResponseBuilder().with_status_code(int(HttpStatus.OK)).with_data(result).build()
