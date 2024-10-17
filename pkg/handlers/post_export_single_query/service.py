from typing import List
from pkg.shared.entity.export.models import SearchExportRequestPayload
from pkg.shared.entity.export.single_query.async_task import SingleQueryExportAsyncTask
from pkg.shared.entity.search.single_query.async_task import SingleQueryAsyncTask
from pkg.shared.entity.search.single_query.model import SingleAlignedPeptide
from pkg.shared.helpers.http.error import ResourceNotFoundException, ConflictException, BadRequestException
from pkg.shared.utils.async_task import AsyncTaskStatus


def get_export_single_query_task_status(task_id: str) -> AsyncTaskStatus[List[SingleAlignedPeptide], Exception]:
    cached_search_task = SingleQueryAsyncTask.get_status(task_id)
    if cached_search_task is None:
        raise ResourceNotFoundException(f'Single query search task {task_id} does not exist.')

    if cached_search_task.loading:
        raise ConflictException(f'Single query search task {task_id} has not finished yet.')

    if not cached_search_task.success:
        raise BadRequestException(f'Single query search task {task_id} was not successful.')

    return cached_search_task


def create_export_single_query_task(payload: SearchExportRequestPayload, cached_task_status: AsyncTaskStatus[List[SingleAlignedPeptide], Exception]) -> SingleQueryExportAsyncTask:
    task = SingleQueryExportAsyncTask(payload, cached_task_status)
    task.start()

    return task
