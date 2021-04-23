import time
from LogEntry import LogEntry, Status


class LogFile:

    logEntries = []
    warningLogs = []
    errorLogs = []

    def __init__(self, filepath="mock_data.txt"):
        self.filepath = filepath  # this is just a string

    def get_error_logs(self):
        return [self.logEntries[i] for i in self.errorLogs]

    def get_warning_logs(self):
        return [self.logEntries[i] for i in self.warningLogs]

    def _follow(self, file):
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def monitor_file(self):

        with open(self.filepath, 'r') as f:
            for line in self._follow(f):
                if line:
                    newLog = LogEntry(len(self.logEntries), line.strip())
                    if newLog.status == Status.WARN:
                        self.warningLogs.append(len(self.logEntries))
                    elif newLog.status == Status.ERROR:
                        self.errorLogs.append(len(self.logEntries))

                    self.logEntries.append(newLog)
