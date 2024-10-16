import dataclasses
from typing import Optional, Dict, Any
from pkg.shared.entity.export.redis import get_async_task_redis_client
from pkg.shared.entity.export.models import SearchExportRequestPayload, SearchExportResult
from pkg.shared.entity.export.utils import create_zip_archive
from pkg.shared.entity.peptide.models import BasePeptide
from pkg.shared.utils.async_task import AsyncTask, AsyncTaskStatus
from pkg.shared.utils.export import base64_to_bit_array


class TextQueryExportAsyncTask(AsyncTask[Dict[str, Any], Exception]):
    TASK_NAME = 'export_text_query'

    def __init__(self, payload: SearchExportRequestPayload):
        super().__init__(TextQueryExportAsyncTask.TASK_NAME)

        self.payload = payload

        self.result = None

    @staticmethod
    def get_status(task_id: str) -> Optional[AsyncTaskStatus]:
        cache = get_async_task_redis_client()
        cached = cache.get_task(task_id)

        if cached is None or cached['name'] != TextQueryExportAsyncTask.TASK_NAME:
            return None

        return AsyncTaskStatus(**cached)

    @staticmethod
    def update_status(status: AsyncTaskStatus) -> None:
        cache = get_async_task_redis_client()
        cache.update_task(status.id, dataclasses.asdict(status))

    def handle_archive_progress(self, completed_resource: str) -> None:
        if self.result:
            self.result.done.append(completed_resource)

            status = self.create_status(True, False, self.result.to_dict())
            TextQueryExportAsyncTask.update_status(status)

    def task(self) -> None:
        parsed_bit_array = base64_to_bit_array(self.payload.data)
        peptide_ids = [BasePeptide.format_id(idx) for idx, bit in enumerate(parsed_bit_array) if bit == 1]

        if len(peptide_ids) < 1:
            raise ValueError('At least one peptide needs to be exported.')

        self.result = SearchExportResult(peptide_ids, len(peptide_ids), self.payload.form, [])
        create_zip_archive(self.task_id, peptide_ids, self.payload.form, self.handle_archive_progress)

    def pre_run(self) -> None:
        cache = get_async_task_redis_client()
        cache.create_task(self.task_id, dataclasses.asdict(self.get_init_status()))

        print(f'Started text query export task {self.task_id}')

    def post_run(self) -> None:
        status = self.create_status(False, True, self.result.to_dict())
        TextQueryExportAsyncTask.update_status(status)

        print(f'Finished text query export task {self.task_id}')

    def handle_error(self, error: Exception) -> None:
        status = self.create_status(False, False, str(error))
        TextQueryExportAsyncTask.update_status(status)

        print(f'Error in text query export task {self.task_id}')
        print(error)
