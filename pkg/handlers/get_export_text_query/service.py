from typing import Optional
from pkg.shared.entity.export.text_query.async_task import TextQueryExportAsyncTask
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_export_text_query_task(task_id: str) -> Optional[AsyncTaskStatus]:
    return TextQueryExportAsyncTask.get_status(task_id)
