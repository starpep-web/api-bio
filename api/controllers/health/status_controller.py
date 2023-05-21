from flask import Blueprint
from api.http.response import ResponseBuilder


status_controller = Blueprint('status', __name__, url_prefix='/status')


@status_controller.route('/', methods=['GET'])
def get_status():
    return ResponseBuilder().with_data('OK').build()
