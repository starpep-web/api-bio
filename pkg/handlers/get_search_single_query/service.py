from typing import Optional
from pkg.shared.entity.search.single_query.async_task import SingleQueryAsyncTask
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_single_query_task(task_id: str) -> Optional[AsyncTaskStatus]:
    return SingleQueryAsyncTask.get_status(task_id)
