import math
from dataclasses import dataclass
from typing import TypeVar, Generic, List
from fastapi import Request
from pkg.shared.error.codes import ErrorCode
from pkg.shared.helpers.http.error import BadRequestException


_T = TypeVar("_T")


_DEFAULT_LIMIT = 100


@dataclass
class PaginationRequest:
    page: int
    limit: int
    start: int


@dataclass
class Pagination:
    currentIndex: int
    total: int
    currentPage: int
    totalPages: int
    previousStart: int
    nextStart: int
    isFirstPage: bool
    isLastPage: bool


@dataclass
class WithPagination(Generic[_T]):
    data: List[_T]
    pagination: Pagination


NULL_PAGINATION = Pagination(
    currentIndex=0,
    total=0,
    currentPage=1,
    totalPages=0,
    previousStart=0,
    nextStart=0,
    isFirstPage=True,
    isLastPage=True
)


def _validate_create_pagination_parameters(start: int, total: int, step: int) -> None:
    if not isinstance(start, int) or start < 0:
        raise BadRequestException('Start must be a positive integer.', ErrorCode.INVALID_QUERY_PROVIDED)

    if not isinstance(total, int) or total < 0:
        raise BadRequestException('Total must be a positive integer.', ErrorCode.INVALID_QUERY_PROVIDED)

    if not isinstance(step, int) or step < 1:
        raise BadRequestException('Step must be a non-zero positive integer.', ErrorCode.INVALID_QUERY_PROVIDED)

    if total != 0 and start >= total:
        raise BadRequestException('Start must be lesser than total. Make sure you have passed a valid page in query parameters.', ErrorCode.INVALID_QUERY_PROVIDED)


def create_pagination(start: int, total: int, step: int) -> Pagination:
    _validate_create_pagination_parameters(start, total, step)
    current_page = 1 if total == 0 else math.floor(start / step) + 1
    total_pages = math.ceil(total / step)

    return Pagination(
        currentIndex=start,
        total=total,
        currentPage=current_page,
        totalPages=total_pages,
        previousStart=0 if total == 0 else max(start - step, 0),
        nextStart=min(start + step, max((total_pages - 1) * step, 0)),
        isFirstPage=current_page == 1 or total == 0,
        isLastPage=current_page == total_pages or total == 0
    )


def resolve_pagination_request(req: Request, limit_fallback: int = _DEFAULT_LIMIT) -> PaginationRequest:
    try:
        min_limit = 10
        max_limit = 100
        default_page = 1

        page_param = req.query_params.get('page') or default_page
        limit_param = req.query_params.get('limit') or limit_fallback

        page = max(int(page_param), default_page)
        limit = min(max(int(limit_param), min_limit), max_limit)
        start = (page - 1) * limit

        return PaginationRequest(
            page=page,
            start=start,
            limit=limit
        )
    except Exception as e:
        raise BadRequestException(str(e), ErrorCode.INVALID_QUERY_PROVIDED)


def paginate_list(arr: List[_T], page: int, limit: int = _DEFAULT_LIMIT) -> WithPagination[_T]:
    start = (page - 1) * limit
    pagination = create_pagination(start, len(arr), limit)
    sliced_list = arr[start:start + limit]

    return WithPagination(sliced_list, pagination)
