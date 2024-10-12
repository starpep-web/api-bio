import math
from dataclasses import dataclass
from typing import TypeVar, Generic, List, Any


T = TypeVar('T')

DEFAULT_STEP = 50


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
class WithPagination(Generic[T]):
    data: T
    pagination: Pagination


def _validate_create_pagination_parameters(start: int, total: int, step: int):
    if not isinstance(start, int) or start < 0:
        raise ValueError('Start must be a positive integer.')

    if not isinstance(total, int) or total < 0:
        raise ValueError('Total must be a positive integer.')

    if not isinstance(step, int) or step < 1:
        raise ValueError('Step must be a non-zero positive integer.')

    if total != 0 and start >= total:
        raise ValueError('Start must be lesser than total.')


def create_pagination(start: int, total: int, step: int) -> Pagination:
    _validate_create_pagination_parameters(start, total, step)
    current_page = 1 if total == 0 else math.floor(start / step) + 1
    total_pages = math.ceil(total / step)

    previous_start = 0 if total == 0 else max(start - step, 0)
    next_start = min(start + step, max((total_pages - 1) * step, 0))

    is_first_page = current_page == 1 or total == 0
    is_last_page = current_page == total_pages or total == 0

    return Pagination(
        currentIndex=start,
        total=total,
        currentPage=current_page,
        totalPages=total_pages,
        previousStart=previous_start,
        nextStart=next_start,
        isFirstPage=is_first_page,
        isLastPage=is_last_page
    )


def paginate_list(arr: List[Any], page: int, limit: int = DEFAULT_STEP) -> WithPagination[List[Any]]:
    start = (page - 1) * limit
    pagination = create_pagination(start, len(arr), limit)
    sliced_list = arr[start:start + limit]

    return WithPagination(sliced_list, pagination)
