import uuid
from typing import TypeVar, Generic
from threading import Thread
from abc import abstractmethod, ABC


T = TypeVar('T')


class AsyncTask(ABC, Thread, Generic[T]):
    def __init__(self):
        super().__init__()
        self.task_id = str(uuid.uuid4())

    @abstractmethod
    def get_init_status(self) -> T:
        pass

    @abstractmethod
    def task(self) -> None:
        pass

    def handle_error(self, error: Exception) -> None:
        pass

    def pre_run(self) -> None:
        pass

    def post_run(self) -> None:
        pass

    def run(self) -> None:
        try:
            self.pre_run()
            self.task()
            self.post_run()
        except Exception as e:
            self.handle_error(e)
