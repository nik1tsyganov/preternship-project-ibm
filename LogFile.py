import re
from enum import Enum
from LogEntry import Status
from SysstatLogEntry import Sysstat
from PrimeradiantLogEntry import Primeradiant
from Qa1080tiLogEntry import QA
import itertools


class Type(Enum):
    SYSSTAT = Sysstat
    PRIME = Primeradiant
    QA1080TI = QA
    UNKNOWN = Sysstat


class LogFile:
    logEntries = []
    warningLogs = []
    errorLogs = []
    fileType = Type.UNKNOWN

    def __init__(self, filepath):
        self.filepath = filepath  # this is just a string
        self._type_of_file()

    def _type_of_file(self):

        topOfFile = ""

        with open(self.filepath, 'r', encoding="latin-1") as file:
            for line in itertools.islice(file, 0, 20):
                topOfFile += line.strip("\n").lower()

        if topOfFile.find("panasas") != -1:
            self.fileType = Type.SYSSTAT
        elif topOfFile.find("primeradiant") != -1:
            self.fileType = Type.PRIME
        elif re.search(r"\[\w{2};\w{3}", topOfFile):
            self.fileType = Type.QA1080TI
        else:
            self.fileType = Type.SYSSTAT

    def monitor_file(self):
        with open(self.filepath, 'r', encoding="latin-1") as f:
            for line in f:
                if (len(self.logEntries) > 0
                        and self.fileType.value.belongs_prev(line)):
                    self.logEntries[-1].data += " " + line.strip()
                    continue

                newLog = self.fileType.value(len(self.logEntries), line)

                if newLog.status == Status.WARN:
                    self.warningLogs.append(len(self.logEntries))
                elif newLog.status == Status.ERROR:
                    self.errorLogs.append(len(self.logEntries))

                self.logEntries.append(newLog)

            return self.logEntries, self.errorLogs, self.warningLogs
