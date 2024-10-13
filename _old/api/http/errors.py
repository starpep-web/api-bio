from typing import Tuple
from flask import Response
from werkzeug.exceptions import HTTPException
from http_constants.status import HttpStatus
from .response import ResponseBuilder

class BadRequestException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'The server could not understand your request.', int(HttpStatus.BAD_REQUEST))


class ConflictException(BaseApiException):
    def __init__(self, message: str):
        BaseApiException.__init__(self, message, 'The server could not fulfill your request at this time.', int(HttpStatus.CONFLICT))
