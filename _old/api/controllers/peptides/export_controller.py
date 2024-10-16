from flask import Blueprint, request
from api.http.response import ResponseBuilder
from api.http.errors import BadRequestException, ResourceNotFoundException, ConflictException
from services.export.payload import SearchExportRequestPayload
from services.export.text_query import TextQueryExportAsyncTask
from services.export.single_query import SingleQueryExportAsyncTask
from services.alignment.single_query import SingleQueryAsyncTask
from services.export.multi_query import MultiQueryExportAsyncTask
from services.alignment.multi_query import MultiQueryAsyncTask


export_controller = Blueprint('export', __name__, url_prefix='/export')


@export_controller.route('/text-query/<task_id>', methods=['GET'])
def get_text_query_export_task(task_id: str):
    cached_task = TextQueryExportAsyncTask.get_status(task_id)

    if cached_task is None:
        raise ResourceNotFoundException(f'Text query export task {task_id} does not exist.')

    return ResponseBuilder().with_data(cached_task).build()


@export_controller.route('/single-query/<task_id>', methods=['GET'])
def get_single_query_export_task(task_id: str):
    cached_task = SingleQueryExportAsyncTask.get_status(task_id)

    if cached_task is None:
        raise ResourceNotFoundException(f'Single query export task {task_id} does not exist.')

    return ResponseBuilder().with_data(cached_task).build()


@export_controller.route('/single-query', methods=['POST'])
def post_single_query_export_task():
    try:
        request_payload = SearchExportRequestPayload.from_json(request.json)
    except Exception as e:
        raise BadRequestException(str(e))

    if not request_payload.is_single_query():
        raise BadRequestException('This endpoint only handles exporting single-query searches.')

    cached_search_task = SingleQueryAsyncTask.get_status(request_payload.data)
    if cached_search_task is None:
        raise ResourceNotFoundException(f'Single query search task {request_payload.data} does not exist.')

    if cached_search_task.loading:
        raise ConflictException(f'Single query search task {request_payload.data} has not finished yet.')

    if not cached_search_task.success:
        raise BadRequestException(f'Single query search task {request_payload.data} was not successful.')

    task = SingleQueryExportAsyncTask(request_payload, cached_search_task)
    task.start()

    return ResponseBuilder().with_data(task.get_init_status()).build()


@export_controller.route('/multi-query/<task_id>', methods=['GET'])
def get_multi_query_export_task(task_id: str):
    cached_task = MultiQueryExportAsyncTask.get_status(task_id)

    if cached_task is None:
        raise ResourceNotFoundException(f'Multi query export task {task_id} does not exist.')

    return ResponseBuilder().with_data(cached_task).build()


@export_controller.route('/multi-query', methods=['POST'])
def post_multi_query_export_task():
    try:
        request_payload = SearchExportRequestPayload.from_json(request.json)
    except Exception as e:
        raise BadRequestException(str(e))

    if not request_payload.is_multi_query():
        raise BadRequestException('This endpoint only handles exporting multi-query searches.')

    cached_search_task = MultiQueryAsyncTask.get_status(request_payload.data)
    if cached_search_task is None:
        raise ResourceNotFoundException(f'Multi query search task {request_payload.data} does not exist.')

    if cached_search_task.loading:
        raise ConflictException(f'Multi query search task {request_payload.data} has not finished yet.')

    if not cached_search_task.success:
        raise BadRequestException(f'Multi query search task {request_payload.data} was not successful.')

    task = MultiQueryExportAsyncTask(request_payload, cached_search_task)
    task.start()

    return ResponseBuilder().with_data(task.get_init_status()).build()
