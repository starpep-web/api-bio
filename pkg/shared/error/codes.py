from enum import Enum


class ErrorCode(Enum):
    UNKNOWN_ERROR = 'UNKNOWN_ERROR'
    NOT_FOUND = 'NOT_FOUND'
    INVALID_QUERY_PROVIDED = 'INVALID_QUERY_PROVIDED'
    INVALID_BODY_PROVIDED = 'INVALID_BODY_PROVIDED'
