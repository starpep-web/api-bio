from typing import Tuple
from flask import Response
from werkzeug.exceptions import HTTPException, NotFound
from http_constants.status import HttpStatus
from .response import ResponseBuilder


class BaseApiException(HTTPException):
    def __init__(self, message: str, description: str, status_code: int):
        HTTPException.__init__(self, message)
        self.message = message
        self.description = description
        self.status_code = status_code

    def build_response(self) -> Tuple[Response, int]:
        error = {
            'message': self.message,
            'description': self.description,
            'status': self.status_code
        }

        return ResponseBuilder().with_status_code(self.status_code).with_data(error).build()


class MissingParameterException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'A required parameter was not provided to this endpoint.', int(HttpStatus.BAD_REQUEST))


class InternalServerErrorException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'An unexpected error has ocurred when handling your request.', int(HttpStatus.INTERNAL_SERVER_ERROR))


class ResourceNotFoundException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'The requested resource was not found.', int(HttpStatus.NOT_FOUND))


def handle_exception(exception: Exception):
    if isinstance(exception, BaseApiException):
        return exception.build_response()

    if isinstance(exception, NotFound):
        return ResourceNotFoundException(exception.description).build_response()

    return InternalServerErrorException(str(exception)).build_response()
