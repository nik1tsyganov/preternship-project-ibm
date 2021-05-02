# Log Entry Class
from enum import Enum
import re
from abc import ABC


class Status(Enum):
    OK = 1
    WARN = 2
    ERROR = 3
    UNKNOWN = 4


class LogEntry(ABC):

    errorRegex = re.compile(r"^\s*err(or)?\s*")
    warnRegex = re.compile(r"^\s*warn(ing)?\s*")
    okRegex = re.compile(r"^\s*i(nfo)?\s*")

    status = Status.UNKNOWN

    def __init__(self, index, data):
        self.index = index
        self.data = data
        self.process()

    @staticmethod
    def belongs_prev(data):
        return re.match(r"^\s{10}", data)

    def process(self):

        if self.errorRegex.match(self.data):
            self.status = Status.ERROR
        elif self.warnRegex.match(self.data):
            self.status = Status.WARN
        elif self.okRegex.match(self.data):
            self.status = Status.OK
        else:
            self.status = Status.UNKNOWN

        return self.status
