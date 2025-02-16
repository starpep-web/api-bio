import dataclasses
from typing import List, Optional, Dict, Any
from Bio import SeqIO
from pkg.shared.entity.peptide.neo4j import get_all_peptides
from pkg.shared.entity.search.redis import get_async_task_redis_client
from pkg.shared.helpers.bio.alignment import replace_ambiguous_amino_acids
from pkg.shared.entity.search.single_query.alignment import align_single_query
from pkg.shared.entity.search.single_query.model import SingleAlignmentOptions
from pkg.shared.utils.async_task import AsyncTask, AsyncTaskStatus


_TContext = Dict[str, Any]
_TData = List[Dict[str, Any]]


class SingleQueryAsyncTask(AsyncTask[_TContext, _TData, Exception]):
    TASK_NAME = 'single_query'

    def __init__(self, query_record: SeqIO.SeqRecord, options: SingleAlignmentOptions):
        super().__init__(SingleQueryAsyncTask.TASK_NAME)

        self.query_record = query_record
        self.options = options

        self.result = None

    @staticmethod
    def get_status(task_id: str) -> Optional[AsyncTaskStatus]:
        cache = get_async_task_redis_client()
        cached = cache.get_task(task_id)

        if cached is None or cached['name'] != SingleQueryAsyncTask.TASK_NAME:
            return None

        return AsyncTaskStatus(**cached)

    @staticmethod
    def update_status(status: AsyncTaskStatus) -> None:
        cache = get_async_task_redis_client()
        cache.update_task(status.id, dataclasses.asdict(status))

    def task(self) -> None:
        peptides = get_all_peptides().as_mapped_object()

        fixed_query = replace_ambiguous_amino_acids(self.query_record.seq)
        self.result = align_single_query(peptides, fixed_query, self.options)

    def pre_run(self) -> None:
        cache = get_async_task_redis_client()
        cache.create_task(self.task_id, dataclasses.asdict(self.get_init_status()))

        print(f'Started single query alignment task {self.task_id}')

    def post_run(self) -> None:
        parsed_result = [dataclasses.asdict(r) for r in self.result]
        status = self.create_status(False, True, dataclasses.asdict(self.options),  parsed_result)
        SingleQueryAsyncTask.update_status(status)

        print(f'Finished single query alignment task {self.task_id}')

    def handle_error(self, error: Exception) -> None:
        status = self.create_status(False, False, dataclasses.asdict(self.options), str(error))
        SingleQueryAsyncTask.update_status(status)

        print(f'Error in single query alignment task {self.task_id}')
        print(error)
