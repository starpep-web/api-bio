from typing import Optional
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.status import HttpStatus


class ApiResponseException(Exception):
    def __init__(self, message: str, description: str, status: HttpStatus, code: Optional[ErrorCode]):
        Exception.__init__(self, message)

        self.name = self.__class__.__name__
        self.message = message
        self.status = status
        self.description = description
        self.code = code or ErrorCode.UNKNOWN_ERROR

    def get_response_payload(self) -> object:
        return {'code': self.code.value, 'message': self.message, 'description': self.description}


class InternalServerException(ApiResponseException):
    def __init__(self, message: Optional[str], code: Optional[ErrorCode]):
        ApiResponseException.__init__(
            self,
            message or 'An unknown error occurred.',
            'Something unexpected happened when handling your request.',
            HttpStatus.INTERNAL_SERVER_ERROR,
            code
        )
