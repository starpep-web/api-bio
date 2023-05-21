from flask import Blueprint
from api.http.response import ResponseBuilder


search_controller = Blueprint('search', __name__, url_prefix='/search')


@search_controller.route('/single-query', methods=['GET'])
def search_single_query():
    return ResponseBuilder().with_data('OK').build()
