from typing import Protocol, Union
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.error import ApiResponseException, InternalServerException, ResourceNotFoundException
from pkg.shared.helpers.http.response import ResponseBuilder


class ErrorLike(Protocol):
    def __init__(self):
        self.message = ''

    def to_api_response_exception(self) -> ApiResponseException:
        pass


def _resolve_api_response_exception(error: Union[ErrorLike, Exception]) -> ApiResponseException:
    if isinstance(error, ApiResponseException):
        return error

    if hasattr(error, 'to_api_response_exception') and callable(error.to_api_response_exception):
        return error.to_api_response_exception()

    return InternalServerException(str(error))


def register_error_handler(app: FastAPI) -> None:
    @app.api_route(path='/{full_path:path}', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD'])
    async def handle_catch_all(req: Request) -> None:
        raise ResourceNotFoundException('This route is not handled by the server.', ErrorCode.NOT_FOUND)

    @app.exception_handler(Exception)
    async def handle_error(req: Request, error: Exception) -> object:
        api_exception = _resolve_api_response_exception(error)
        response = ResponseBuilder().with_error(api_exception)
        return JSONResponse(content=response.build(), status_code=response.code)
