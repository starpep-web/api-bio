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

@export_controller.route('/multi-query/<task_id>', methods=['GET'])
def get_multi_query_export_task(task_id: str):
    cached_task = MultiQueryExportAsyncTask.get_status(task_id)

    if cached_task is None:
        raise ResourceNotFoundException(f'Multi query export task {task_id} does not exist.')

    return ResponseBuilder().with_data(cached_task).build()
