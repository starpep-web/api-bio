from typing import Optional
from pkg.shared.entity.search.single_query.async_task import SingleQueryAsyncTask
from pkg.shared.utils.async_task import AsyncTaskStatus
from pkg.shared.utils.lang import safe_int
from pkg.shared.utils.pagination import paginate_list


def get_single_query_task(task_id: str) -> Optional[AsyncTaskStatus]:
    return SingleQueryAsyncTask.get_status(task_id)


def get_paginated_task_data(cached_task_status: AsyncTaskStatus, page_param: Optional[str]) -> object:
    page = safe_int(page_param) or 1
    return {**cached_task_status.__dict__, 'data': paginate_list(cached_task_status.data, page)}
