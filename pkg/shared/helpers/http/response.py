from typing import Union
from pkg.shared.helpers.http.error import ApiResponseException
from pkg.shared.helpers.http.status import HttpStatus

FIRST_UNSUCCESSFUL_STATUS_CODE = 400

ValidData = Union[object, str, int, float, bool, None]


class ResponseBuilder:
    def __init__(self):
        self.success = True
        self.status = HttpStatus.OK
        self.data = None
        self.error = None

    def with_status_code(self, status: HttpStatus) -> 'ResponseBuilder':
        self.status = status
        self.success = status.value < FIRST_UNSUCCESSFUL_STATUS_CODE
        return self

    def with_data(self, data: ValidData) -> 'ResponseBuilder':
        self.data = data
        return self

    def with_error(self, error: ApiResponseException) -> 'ResponseBuilder':
        self.error = error.get_response_payload()
        return self.with_status_code(error.status)

    def build(self) -> object:
        if self.error is not None:
            return {'status': self.status.value, 'success': self.success, 'error': self.error}

        return {'status': self.status.value, 'success': self.success, 'data': self.data}

    @property
    def code(self) -> int:
        return self.status.value
