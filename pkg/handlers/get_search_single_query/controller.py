from fastapi import Request, Response
from pkg.handlers import router
from pkg.handlers.get_search_single_query.service import get_search_single_query_task
from pkg.shared.entity.search.utils import get_paginated_task_data
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.error import ResourceNotFoundException, BadRequestException
from pkg.shared.helpers.http.response import ResponseBuilder
from pkg.shared.helpers.http.status import HttpStatus


@router.get('/search/single-query/{task_id}')
async def get(req: Request, res: Response, task_id: str):
    cached_task_status = get_search_single_query_task(task_id)
    if not cached_task_status:
        raise ResourceNotFoundException(f'Single query search task {task_id} does not exist.', ErrorCode.NOT_FOUND)

    if cached_task_status.loading or not cached_task_status.success:
        return ResponseBuilder().with_data(cached_task_status).build()

    try:
        page_param = req.query_params.get('page')
        data = get_paginated_task_data(cached_task_status, page_param)
    except Exception as e:
        raise BadRequestException(str(e), ErrorCode.INVALID_QUERY_PROVIDED)

    response = ResponseBuilder().with_status_code(HttpStatus.OK).with_data(data)

    res.status_code = response.code
    return response.build()
