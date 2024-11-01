from typing import List
from pkg.shared.entity.export.models import SearchExportRequestPayload
from pkg.shared.entity.export.multi_query.async_task import MultiQueryExportAsyncTask
from pkg.shared.entity.search.multi_query.async_task import MultiQueryAsyncTask
from pkg.shared.entity.search.multi_query.model import MultiAlignedPeptide
from pkg.shared.helpers.http.error import ResourceNotFoundException, ConflictException, BadRequestException
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_export_multi_query_task_status(task_id: str) -> AsyncTaskStatus[List[MultiAlignedPeptide], Exception]:
    cached_search_task = MultiQueryAsyncTask.get_status(task_id)
    if cached_search_task is None:
        raise ResourceNotFoundException(f'Multi query search task {task_id} does not exist.')

    if cached_search_task.loading:
        raise ConflictException(f'Multi query search task {task_id} has not finished yet.')

    if not cached_search_task.success:
        raise BadRequestException(f'Multi query search task {task_id} was not successful.')

    return cached_search_task


def create_export_multi_query_task(payload: SearchExportRequestPayload, cached_task_status: AsyncTaskStatus[List[MultiAlignedPeptide], Exception]) -> MultiQueryExportAsyncTask:
    task = MultiQueryExportAsyncTask(payload, cached_task_status)
    task.start()

    return task
