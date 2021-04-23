# Log Entry Class
from enum import Enum


class Status(Enum):
    OK = 1
    WARN = 2
    ERROR = 3
    UNKNOWN = 4


class LogEntry:
    status = Status.UNKNOWN

    def __init__(self, index, data):
        self.index = index
        self.data = data
        self.process()

    def process(self):
        # TODO : write function that process the data (string) to get the status of a given log entry
        # can use self.data to access the string

        print(self.data)

        return self.status
