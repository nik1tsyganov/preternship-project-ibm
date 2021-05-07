# Log Entry Class
from enum import Enum
from abc import ABC, abstractmethod


class Status(Enum):
    OK = 1
    WARN = 2
    ERROR = 3
    UNKNOWN = 4


class LogEntry(ABC):
    status = Status.UNKNOWN

    def __init__(self, index, data):
        self.index = index
        self.data = data
        self.process()

    @staticmethod
    def belongs_prev(data):
        pass

    @abstractmethod
    def process(self):

        pass
