import time
import re
from enum import Enum
from LogEntry import LogEntry, Status
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

    def get_error_logs(self):
        return [self.logEntries[i] for i in self.errorLogs]

    def get_warning_logs(self):
        return [self.logEntries[i] for i in self.warningLogs]

    def _follow(self, file):
        while True:
            line = file.readline()
            yield line

    def _type_of_file(self):

        topOfFile = ""

        with open(self.filepath, 'r') as file:
            for line in itertools.islice(file, 0, 20):
                topOfFile += line.strip("\n").lower()

        print(topOfFile)

        if topOfFile.find("panasas") != -1:
            self.fileType = Type.SYSSTAT
        elif topOfFile.find("primeradiant") != -1:
            self.fileType = Type.PRIME
        elif re.match(r"[a-f0-9]{2};[0-9a-f]{3}", topOfFile):
            self.fileType = Type.QA1080TI
        else:
            self.fileType = Type.SYSSTAT

        print(self.fileType)

    def monitor_file(self, callback):

        sleep_counter = 0

        with open(self.filepath, 'r') as f:
            for line in self._follow(f):
                if sleep_counter == 5:
                    callback(self.logEntries, self.get_error_logs(), self.get_warning_logs())

                if line:
                    if Sysstat.belongs_prev(line) and self.fileType == Type.SYSSTAT:
                        newLog.data = newLog.data + " " + line.strip()

                    else:
                        if self.fileType == Type.SYSSTAT:
                            newLog = Sysstat(len(self.logEntries), line.strip("\n").lower())
                        elif self.fileType == Type.PRIME:
                            newLog = Primeradiant(len(self.logEntries), line.strip("\n").lower())
                        elif self.fileType == Type.QA1080TI:
                            newLog = QA(len(self.logEntries), line.strip("\n").lower())
                        else:
                            newLog = Sysstat(len(self.logEntries), line.strip("\n").lower())

                    if newLog.status == Status.WARN:
                        self.warningLogs.append(len(self.logEntries))
                    elif newLog.status == Status.ERROR:
                        self.errorLogs.append(len(self.logEntries))

                    self.logEntries.append(newLog)
                    sleep_counter = 0

                else:
                    sleep_counter += 1
                    time.sleep(0.1)
