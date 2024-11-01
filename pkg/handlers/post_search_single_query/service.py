from Bio import SeqIO
from pkg.shared.entity.search.single_query.model import SingleAlignmentOptions
from pkg.shared.entity.search.single_query.async_task import SingleQueryAsyncTask


def create_search_single_query_task(query_record: SeqIO.SeqRecord, options: SingleAlignmentOptions) -> SingleQueryAsyncTask:
    task = SingleQueryAsyncTask(query_record, options)
    task.start()

    return task