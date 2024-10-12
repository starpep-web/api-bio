from __future__ import annotations
from typing import Tuple
from flask import jsonify, Response
from http_constants.status import HttpStatus


class ResponseBuilder:
    def __init__(self):
        self._body = {}
        self._status = int(HttpStatus.OK)

    def with_status_code(self, status_code: int) -> ResponseBuilder:
        self._status = status_code
        return self

    def with_data(self, data: object) -> ResponseBuilder:
        self._body = data
        return self

    def build(self) -> Tuple[Response, int]:
        return jsonify(self._body), self._status
