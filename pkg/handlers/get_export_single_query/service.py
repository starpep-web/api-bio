from typing import Optional
from pkg.shared.entity.export.single_query.async_task import SingleQueryExportAsyncTask
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_export_single_query_task(task_id: str) -> Optional[AsyncTaskStatus]:
    return SingleQueryExportAsyncTask.get_status(task_id)
