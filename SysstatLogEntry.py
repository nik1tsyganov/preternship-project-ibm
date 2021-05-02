import re
from LogEntry import LogEntry, Status


class Sysstat(LogEntry):

    errorRegex = re.compile(r"^\s*err(or)?\s*")
    warnRegex = re.compile(r"^\s*warn(ing)?\s*")
    okRegex = re.compile(r"^\s*info(rmation)?\s*")

    def __init__(self, index, data):
        LogEntry.__init__(self, index, data)

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
