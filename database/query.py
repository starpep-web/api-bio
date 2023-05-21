from __future__ import annotations
from typing import Generic, TypeVar, Callable, Dict, Any, List, Optional
from py2neo.cypher import Cursor
import pandas as pd
import numpy as np


T = TypeVar('T')


class QueryWrapper(Generic[T]):
    def __init__(self, cursor: Cursor, mapper_fn: Callable[[QueryWrapper[T]], T] = None):
        self._cursor = cursor
        self.mapper_fn = mapper_fn

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    def as_data(self) -> List[Dict[Any, Any]]:
        return self._cursor.data()

    def as_df(self) -> pd.DataFrame:
        return self._cursor.to_data_frame()

    def as_np(self) -> np.array:
        return self._cursor.to_ndarray()

    def as_mapped_object(self) -> Optional[T]:
        if not self.mapper_fn:
            return None

        return self.mapper_fn(self)
