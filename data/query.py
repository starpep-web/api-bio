from py2neo.cypher import Cursor
import pandas as pd
import numpy as np


class QueryWrapper:
    def __init__(self, cursor: Cursor):
        self._cursor = cursor

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    def as_df(self) -> pd.DataFrame:
        return self._cursor.to_data_frame()

    def as_np(self) -> np.array:
        return self._cursor.to_ndarray()
