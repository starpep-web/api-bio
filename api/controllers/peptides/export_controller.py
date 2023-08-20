from flask import Blueprint, request
from api.http.response import ResponseBuilder
from api.http.errors import BadRequestException, ResourceNotFoundException
from services.export.payload import SearchExportRequestPayload
from services.export.text_query import TextQueryExportAsyncTask


export_controller = Blueprint('export', __name__, url_prefix='/export')


@export_controller.route('/text-query/<task_id>', methods=['GET'])
def get_text_query_export_task(task_id: str):
    cached_task = TextQueryExportAsyncTask.get_status(task_id)

    if cached_task is None:
        raise ResourceNotFoundException(f'Text query export task {task_id} does not exist.')

    return ResponseBuilder().with_data(cached_task).build()


@export_controller.route('/text-query', methods=['POST'])
def post_text_query_export_task():
    try:
        request_payload = SearchExportRequestPayload.from_json(request.json)
    except Exception as e:
        raise BadRequestException(str(e))

    if not request_payload.is_text():
        raise BadRequestException('This endpoint only handles exporting text-query searches.')

    task = TextQueryExportAsyncTask(request_payload)
    task.start()

    return ResponseBuilder().with_data(task.get_init_status()).build()
