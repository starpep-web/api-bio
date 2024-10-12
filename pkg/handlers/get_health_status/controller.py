from fastapi import Response
from pkg.handlers import router
from pkg.shared.helpers.http.response import ResponseBuilder
from pkg.shared.helpers.http.status import HttpStatus
from pkg.handlers.get_health_status.service import get_status_message


@router.get('/health/status')
def get(res: Response):
    response = ResponseBuilder().with_status_code(HttpStatus.OK).with_data(get_status_message())

    res.status_code = response.code
    return response.build()
