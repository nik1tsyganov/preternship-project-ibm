import time
from LogEntry import LogEntry, Status


def follow(thefile):
    #thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


class LogFile:

    logEntries = []
    warningLogs = []
    errorLogs = []

    def __init__(self, filepath="mock_data.txt"):
        self.filepath = filepath

    def get_error_logs(self):
        return [self.logEntries[i] for i in self.errorLogs]

    def get_warning_logs(self):
        return [self.logEntries[i] for i in self.warningLogs]

    def monitor_file(self):

        with open(self.filepath, 'r') as f:
            for line in follow(f):
                if line:
                    newLog = LogEntry(len(self.logEntries), line.strip())
                    if newLog.status == Status.WARN:
                        self.warningLogs.append(len(self.logEntries))
                    elif newLog.status == Status.ERROR:
                        self.errorLogs.append(len(self.logEntries))

                    self.logEntries.append(newLog)
