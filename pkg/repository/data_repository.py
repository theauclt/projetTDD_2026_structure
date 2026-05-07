from typing import List

from pandas import DataFrame, read_csv

from pkg.models.match import Match


class DataRepository:

    def __init__(self, file, adapter, sep=";"):
        self.adapter = adapter
        self.file = file
        self.sep = sep

    def load(self) -> List[Match]:
        self.df = read_csv(self.file, sep=self.sep)
        return [self.adapter.adapt(row) for _, row in self.df.iterrows()]

    def save(self, objects):
        rows = [self.adapter.to_row(obj) for obj in objects]
        df = DataFrame(rows)
        df.to_csv(self.file, index=False)
