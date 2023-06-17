import uuid
from typing import TypeVar, Generic, Union, Optional
from threading import Thread
from abc import abstractmethod, ABC
from dataclasses import dataclass


S = TypeVar('S')
E = TypeVar('E', bound=Exception)


@dataclass
class AsyncTaskStatus(Generic[S, E]):
    id: str
    name: str
    loading: bool
    success: bool
    data: Optional[Union[S, E]]


class AsyncTask(ABC, Thread, Generic[S, E]):
    def __init__(self, name: str):
        super().__init__()
        self.task_id = str(uuid.uuid4())
        self.name = name

    @abstractmethod
    def task(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_status(task_id: str) -> AsyncTaskStatus[S, Union[E, str]]:
        pass

    @staticmethod
    @abstractmethod
    def update_status(status: AsyncTaskStatus[S, Union[E, str]]) -> None:
        pass

    def create_status(self, loading: bool, success: bool, data: Union[S, E, str]) -> AsyncTaskStatus[S, Union[E, str]]:
        return AsyncTaskStatus(self.task_id, self.name, loading, success, data)

    def get_init_status(self) -> AsyncTaskStatus[S, Union[E, str]]:
        return self.create_status(True, False, None)

    def initialize(self) -> AsyncTaskStatus[S, Union[E, str]]:
        return self.get_init_status()

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
