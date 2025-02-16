import uuid
from typing import TypeVar, Generic, Union, Optional
from threading import Thread
from abc import abstractmethod, ABC
from dataclasses import dataclass


_TContext = TypeVar('_TContext')
_TData = TypeVar('_TData')
_TException = TypeVar('_TException', bound=Exception)


@dataclass
class AsyncTaskStatus(Generic[_TContext, _TData, _TException]):
    id: str
    name: str
    loading: bool
    success: bool
    context: Optional[_TContext]
    data: Optional[Union[_TData, _TException]]


class AsyncTask(ABC, Thread, Generic[_TContext, _TData, _TException]):
    def __init__(self, name: str):
        super().__init__()
        self.task_id = str(uuid.uuid4())
        self.name = name

    @abstractmethod
    def task(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_status(task_id: str) -> AsyncTaskStatus[_TContext, _TData, Union[_TException, str]]:
        pass

    @staticmethod
    @abstractmethod
    def update_status(status: AsyncTaskStatus[_TContext, _TData, Union[_TException, str]]) -> None:
        pass

    def create_status(self, loading: bool, success: bool, context: Optional[_TContext], data: Union[_TData, _TException, str]) -> AsyncTaskStatus[_TContext, _TData, Union[_TException, str]]:
        return AsyncTaskStatus(self.task_id, self.name, loading, success, context, data)

    def get_init_status(self) -> AsyncTaskStatus[_TContext, _TData, Union[_TException, str]]:
        return self.create_status(True, False, None, None)

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
