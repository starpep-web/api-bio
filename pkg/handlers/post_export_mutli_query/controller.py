from fastapi import Response
from pkg.handlers import router
from pkg.handlers.post_export_mutli_query.service import get_export_multi_query_task_status, create_export_multi_query_task
from pkg.shared.entity.export.models import SearchExportRequestPayload
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.error import BadRequestException
from pkg.shared.helpers.http.response import ResponseBuilder
from pkg.shared.helpers.http.status import HttpStatus


@router.post('/export/multi-query')
async def post(res: Response, payload: SearchExportRequestPayload):
    if not payload.is_multi_query():
        raise BadRequestException('This endpoint only handles exporting multi-query searches.', ErrorCode.INVALID_BODY_PROVIDED)

    cached_search_task_status = get_export_multi_query_task_status(payload.data)
    task = create_export_multi_query_task(payload, cached_search_task_status)
    response = ResponseBuilder().with_status_code(HttpStatus.CREATED).with_data(task.get_init_status())

    res.status_code = response.code
    return response.build()
