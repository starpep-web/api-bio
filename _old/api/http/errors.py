from typing import Tuple
from flask import Response
from werkzeug.exceptions import HTTPException
from http_constants.status import HttpStatus
from .response import ResponseBuilder

class MissingParameterException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'A required parameter was not provided to this endpoint.', int(HttpStatus.BAD_REQUEST))


class ResourceNotFoundException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'The requested resource was not found.', int(HttpStatus.NOT_FOUND))


class BadRequestException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'The server could not understand your request.', int(HttpStatus.BAD_REQUEST))


class ConflictException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'The server could not fulfill your request at this time.', int(HttpStatus.CONFLICT))


def handle_exception(exception: Exception):
    if isinstance(exception, BaseApiException):
        return exception.build_response()

    if isinstance(exception, HTTPException):
        return BaseApiException(exception.description, 'The server could not handle your request.', exception.code or int(HttpStatus.INTERNAL_SERVER_ERROR)).build_response()


    return InternalServerErrorException(str(exception)).build_response()
