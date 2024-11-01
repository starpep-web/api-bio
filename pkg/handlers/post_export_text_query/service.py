from pkg.shared.entity.export.models import SearchExportRequestPayload
from pkg.shared.entity.export.text_query.async_task import TextQueryExportAsyncTask


def create_export_text_query_task(payload: SearchExportRequestPayload) -> TextQueryExportAsyncTask:
    task = TextQueryExportAsyncTask(payload)
    task.start()

    return task
