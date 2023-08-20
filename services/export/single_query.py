import dataclasses
from typing import Dict, Any, Optional, List
from services.cache import cache
from lib.bio.alignment import SingleAlignedPeptide
from services.export.payload import SearchExportRequestPayload, SearchExportResult
from services.export.archive import create_zip_archive
from lib.asynchronous.task import AsyncTask, AsyncTaskStatus, S, E


class SingleQueryExportAsyncTask(AsyncTask[Dict[str, Any], Exception]):
    TASK_NAME = 'export_single_query'

    def __init__(self, payload: SearchExportRequestPayload, search_task: AsyncTaskStatus[List[SingleAlignedPeptide], Exception]):
        super().__init__(SingleQueryExportAsyncTask.TASK_NAME)

        self.payload = payload
        self.search_task = search_task

        self.result = None

    @staticmethod
    def get_status(task_id: str) -> Optional[AsyncTaskStatus[S, E]]:
        cached = cache.export.get_task(task_id)

        if cached is None or cached['name'] != SingleQueryExportAsyncTask.TASK_NAME:
            return None

        return AsyncTaskStatus(**cached)

    @staticmethod
    def update_status(status: AsyncTaskStatus[S, E]) -> None:
        cache.export.update_task(status.id, dataclasses.asdict(status))

    def handle_archive_progress(self, completed_resource: str) -> None:
        if self.result:
            self.result.done.append(completed_resource)

            status = self.create_status(False, True, dataclasses.asdict(self.result))
            SingleQueryExportAsyncTask.update_status(status)

    def task(self) -> None:
        peptide_ids = [peptide['id'] for peptide in self.search_task.data]

        if len(peptide_ids) < 1:
            raise ValueError('At least one peptide needs to be exported.')

        self.result = SearchExportResult(peptide_ids, len(peptide_ids), self.payload.form, [])
        create_zip_archive(self.task_id, peptide_ids, self.payload.form, self.handle_archive_progress)

    def pre_run(self) -> None:
        cache.export.create_task(self.task_id, dataclasses.asdict(self.get_init_status()))

        print(f'Started single query export task {self.task_id}')

    def post_run(self) -> None:
        status = self.create_status(False, True, dataclasses.asdict(self.result))
        SingleQueryExportAsyncTask.update_status(status)

        print(f'Finished single query export task {self.task_id}')

    def handle_error(self, error: Exception) -> None:
        status = self.create_status(False, False, str(error))
        SingleQueryExportAsyncTask.update_status(status)

        print(f'Error in single query export task {self.task_id}')
        print(error)
