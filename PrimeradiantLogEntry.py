import re
from LogEntry import LogEntry, Status


class Primeradiant(LogEntry):

    def __init__(self, index, data):
        LogEntry.__init__(self, index, data)

    @staticmethod
    def belongs_prev(data):
        return False

    def process(self):

        if re.search(r"\s*err(or)?|fail(ure|ed)?\s*", self.data):
            self.status = Status.ERROR
        elif re.search(r"\s*warn(ing)?\s*", self.data):
            self.status = Status.WARN
        else:
            self.status = Status.OK

        return self.status
