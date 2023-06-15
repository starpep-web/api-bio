import dataclasses
from Bio import SeqIO
from services.database import db
from services.cache import cache
from lib.bio.alignment import blosum_align_query, replace_atypical_aas, AlignmentOptions
from lib.asynchronous.task import AsyncTask


# TODO: Change init status return.
class SingleQueryAsyncTask(AsyncTask[str]):
    def __init__(self, query_record: SeqIO.SeqRecord, options: AlignmentOptions):
        super().__init__()

        self.query_record = query_record
        self.options = options

        self.result = None

    def get_init_status(self) -> str:
        return self.task_id

    def task(self) -> None:
        # TODO: Turn this into a generator to improve performance.
        peptides = db.peptides.get_all_peptides().as_mapped_object()

        fixed_query = replace_atypical_aas(self.query_record.seq)
        self.result = blosum_align_query(peptides, fixed_query, self.options)

    def pre_run(self) -> None:
        cache.search.create_task(self.task_id, self.get_init_status())
        print(f'Started single query alignment task {self.task_id}')

    def post_run(self) -> None:
        parsed_result = [dataclasses.asdict(r) for r in self.result]
        cache.search.update_task(self.task_id, parsed_result)
        print(f'Finished single query alignment task {self.task_id}')

    def handle_error(self, error: Exception) -> None:
        cache.search.update_task(self.task_id, str(error))
        print(f'Error in single query aligment task {self.task_id}')
        print(error)
