from typing import Optional
from pkg.shared.entity.export.multi_query.async_task import MultiQueryExportAsyncTask
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_export_multi_query_task(task_id: str) -> Optional[AsyncTaskStatus]:
    return MultiQueryExportAsyncTask.get_status(task_id)
