from abc import ABC, abstractmethod


class BaseAdapter(ABC):

    @abstractmethod
    def adapt(self, row):
        raise NotImplementedError

    @abstractmethod
    def to_row(self, match):
        raise NotImplementedError
