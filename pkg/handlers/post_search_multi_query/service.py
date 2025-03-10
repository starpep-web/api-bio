from Bio import SeqIO
from typing import List
from pkg.shared.entity.search.multi_query.model import MultiAlignmentOptions
from pkg.shared.entity.search.multi_query.async_task import MultiQueryAsyncTask


def create_search_multi_query_task(query_records: List[SeqIO.SeqRecord], query: str, options: MultiAlignmentOptions) -> MultiQueryAsyncTask:
    task = MultiQueryAsyncTask(query_records, query, options)
    task.start()

    return task
