import dataclasses
from typing import List, Optional, Dict, Any, Union
from Bio import SeqIO
from services.database import db
from services.cache import cache
from lib.bio.alignment import align_multi_query, replace_ambiguous_amino_acids, MultiAlignmentOptions
from lib.asynchronous.task import AsyncTask, AsyncTaskStatus, S, E


class MultiQueryAsyncTask(AsyncTask[List[Dict[str, Any]], Exception]):
    TASK_NAME = 'multi_query'

    def __init__(self, query_records: List[SeqIO.SeqRecord], options: MultiAlignmentOptions):
        super().__init__(MultiQueryAsyncTask.TASK_NAME)

        self.query_records = query_records
        self.options = options

        self.result = None

    @staticmethod
    def get_status(task_id: str) -> Optional[AsyncTaskStatus[S, E]]:
        cached = cache.search.get_task(task_id)

        if cached is None or cached['name'] != MultiQueryAsyncTask.TASK_NAME:
            return None

        return AsyncTaskStatus(**cached)

    @staticmethod
    def update_status(status: AsyncTaskStatus[S, E]) -> None:
        cache.search.update_task(status.id, dataclasses.asdict(status))

    def initialize(self) -> AsyncTaskStatus[S, Union[E, str]]:
        cache.search.create_task(self.task_id, dataclasses.asdict(self.get_init_status()))
        return self.get_init_status()

    def pre_run(self) -> None:
        print(f'Started multi query alignment task {self.task_id}')

    def task(self) -> None:
        peptides = db.peptides.get_all_peptides().as_mapped_object()

        fixed_queries = [replace_ambiguous_amino_acids(record.seq) for record in self.query_records]
        self.result = align_multi_query(peptides, fixed_queries, self.options)

    def post_run(self) -> None:
        parsed_result = [dataclasses.asdict(r) for r in self.result]
        status = self.create_status(False, True, parsed_result)
        MultiQueryAsyncTask.update_status(status)

        print(f'Finished multi query alignment task {self.task_id}')

    def handle_error(self, error: Exception) -> None:
        status = self.create_status(False, False, str(error))
        MultiQueryAsyncTask.update_status(status)

        print(f'Error in multi query aligment task {self.task_id}')
        print(error)
