from fastapi import Response
from pkg.handlers import router
from pkg.handlers.get_export_text_query.service import get_export_text_query_task
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.error import ResourceNotFoundException
from pkg.shared.helpers.http.response import ResponseBuilder
from pkg.shared.helpers.http.status import HttpStatus


@router.get('/export/text-query/{task_id}')
async def get(res: Response, task_id: str):
    cached_task_status = get_export_text_query_task(task_id)
    if not cached_task_status:
        raise ResourceNotFoundException(f'Text query export task {task_id} does not exist.', ErrorCode.NOT_FOUND)

    response = ResponseBuilder().with_status_code(HttpStatus.OK).with_data(cached_task_status)

    res.status_code = response.code
    return response.build()
