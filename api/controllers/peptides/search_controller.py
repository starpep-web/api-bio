from flask import Blueprint, request
from api.http.response import ResponseBuilder
from api.http.types import MIME_TYPE_FASTA
from api.http.errors import BadRequestException, ResourceNotFoundException
from lib.bio.fasta import parse_fasta_string, is_single_fasta_valid
from lib.bio.alignment import AlignmentOptions
from services.alignment.single_query import SingleQueryAsyncTask


search_controller = Blueprint('search', __name__, url_prefix='/search')


@search_controller.route('/single-query', methods=['POST'])
def post_single_query_task():
    content_type = request.headers.get('Content-Type')
    if content_type != MIME_TYPE_FASTA:
        raise BadRequestException(f'Invalid request body type provided, must be {MIME_TYPE_FASTA}')

    fasta_query = request.get_data(as_text=True)
    parsed_fasta = parse_fasta_string(fasta_query)
    if not is_single_fasta_valid(parsed_fasta):
        raise BadRequestException('Request body is not valid FASTA.')

    try:
        options = AlignmentOptions.create_from_params(request.args.to_dict())
    except ValueError as e:
        raise BadRequestException(str(e))

    task = SingleQueryAsyncTask(parsed_fasta[0], options)
    task.start()

    return ResponseBuilder().with_data(task.get_init_status()).build()


@search_controller.route('/single-query/<task_id>', methods=['GET'])
def get_single_query_task(task_id: str):
    cached_task = SingleQueryAsyncTask.get_status(task_id)

    if cached_task is None:
        raise ResourceNotFoundException(f'Single query search task {task_id} does not exist.')

    return ResponseBuilder().with_data(cached_task).build()
