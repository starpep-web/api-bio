import dataclasses
from typing import List, Optional, Dict, Any
from Bio import SeqIO
from services.database import db
from services.cache import cache
from lib.bio.alignment import blosum_align_query, replace_atypical_aas, AlignmentOptions
from lib.asynchronous.task import AsyncTask, AsyncTaskStatus, S, E


class SingleQueryAsyncTask(AsyncTask[List[Dict[str, Any]], Exception]):
    TASK_NAME = 'single_query'

    def __init__(self, query_record: SeqIO.SeqRecord, options: AlignmentOptions):
        super().__init__(SingleQueryAsyncTask.TASK_NAME)

        self.query_record = query_record
        self.options = options

        self.result = None

    @staticmethod
    def get_status(task_id: str) -> Optional[AsyncTaskStatus[S, E]]:
        cached = cache.search.get_task(task_id)

        if cached is not None and cached['name'] != SingleQueryAsyncTask.TASK_NAME:
            return None

        return cached

    @staticmethod
    def update_status(status: AsyncTaskStatus[S, E]) -> None:
        cache.search.update_task(status.id, dataclasses.asdict(status))

    def task(self) -> None:
        # TODO: Turn this into a generator to improve performance.
        peptides = db.peptides.get_all_peptides().as_mapped_object()

        fixed_query = replace_atypical_aas(self.query_record.seq)
        self.result = blosum_align_query(peptides, fixed_query, self.options)

    def pre_run(self) -> None:
        cache.search.create_task(self.task_id, dataclasses.asdict(self.get_init_status()))

        print(f'Started single query alignment task {self.task_id}')

    def post_run(self) -> None:
        parsed_result = [dataclasses.asdict(r) for r in self.result]
        status = self.create_status(False, True, parsed_result)
        SingleQueryAsyncTask.update_status(status)

        print(f'Finished single query alignment task {self.task_id}')

    def handle_error(self, error: Exception) -> None:
        status = self.create_status(False, False, str(error))
        SingleQueryAsyncTask.update_status(status)

        print(f'Error in single query aligment task {self.task_id}')
        print(error)
