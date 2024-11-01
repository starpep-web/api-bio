from typing import Optional
from pkg.shared.entity.search.multi_query.async_task import MultiQueryAsyncTask
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_search_multi_query_task(task_id: str) -> Optional[AsyncTaskStatus]:
    return MultiQueryAsyncTask.get_status(task_id)
