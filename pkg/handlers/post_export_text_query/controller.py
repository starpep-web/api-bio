from fastapi import Response
from pkg.handlers import router
from pkg.handlers.post_export_text_query.service import create_export_text_query_task
from pkg.shared.entity.export.models import SearchExportRequestPayload
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.error import BadRequestException
from pkg.shared.helpers.http.response import ResponseBuilder
from pkg.shared.helpers.http.status import HttpStatus


@router.post('/export/text-query')
async def post(res: Response, payload: SearchExportRequestPayload):
    if not payload.is_text():
        raise BadRequestException('This endpoint only handles exporting text-query searches.', ErrorCode.INVALID_BODY_PROVIDED)

    task = create_export_text_query_task(payload)
    response = ResponseBuilder().with_status_code(HttpStatus.CREATED).with_data(task.get_init_status())

    res.status_code = response.code
    return response.build()
