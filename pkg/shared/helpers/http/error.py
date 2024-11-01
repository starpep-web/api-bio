from typing import Optional, List, Any
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.status import HttpStatus


class ApiResponseException(Exception):
    def __init__(self, message: str, description: str, status: HttpStatus, code: Optional[ErrorCode] = None):
        Exception.__init__(self, message)

        self.name = self.__class__.__name__
        self.message = message
        self.status = status
        self.description = description
        self.code = code or ErrorCode.UNKNOWN_ERROR

    def get_response_payload(self) -> object:
        return {'code': self.code.value, 'message': self.message, 'description': self.description}


class InternalServerException(ApiResponseException):
    def __init__(self, message: Optional[str] = None, code: Optional[ErrorCode] = None):
        ApiResponseException.__init__(
            self,
            message or 'An unknown error occurred.',
            'Something unexpected happened when handling your request.',
            HttpStatus.INTERNAL_SERVER_ERROR,
            code
        )


class ConflictException(ApiResponseException):
    def __init__(self, message: str, code: Optional[ErrorCode] = None):
        ApiResponseException.__init__(
            self,
            message,
            'The server could not fulfill your request at this time.',
            HttpStatus.CONFLICT,
            code
        )


class ResourceNotFoundException(ApiResponseException):
    def __init__(self, message: str, code: Optional[ErrorCode] = None):
        ApiResponseException.__init__(
            self,
            message,
            'The requested resource was not found by the server.',
            HttpStatus.NOT_FOUND,
            code
        )


class BadRequestException(ApiResponseException):
    def __init__(self, message: str, code: Optional[ErrorCode] = None):
        ApiResponseException.__init__(
            self,
            message,
            'The server could not handle your request. Please verify that your request is correct and try again.',
            HttpStatus.BAD_REQUEST,
            code
        )


class SchemaValidationException(ApiResponseException):
    def __init__(self, message: str, code: Optional[ErrorCode] = None, issues: Optional[List[Any]] = None):
        ApiResponseException.__init__(
            self,
            message,
            'The body of this request does not conform to the validation schema.',
            HttpStatus.BAD_REQUEST,
            code
        )

        self.issues = issues or []

    def get_response_payload(self) -> object:
        return {**super().get_response_payload(), 'issues': self.issues}
