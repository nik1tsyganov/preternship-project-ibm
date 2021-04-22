import time
import logEntry


def follow(thefile):
    thefile.seek(0, 2)
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

    def __init__(self, filepath="mock_data.clf"):
        self.filepath = filepath

    def get_error_logs(self):
        return [self.logEntries[i] for i in self.errorLogs]

    def get_warning_logs(self):
        return [self.logEntries[i] for i in self.warningLogs]

    def monitor_file(self):

        index = 0
        with open(self.filepath, 'r') as f:
            for line in follow(f):
                if line:
                    newlog = logEntry.process(line.strip(), index)
                    if newlog.status == 'OK':
                        self.logEntries.append(newlog)
                    elif newlog.status == 'Warn':
                        self.warningLogs.append(newlog)
                        self.logEntries.append(newlog)
                    else:
                        self.errorLogs.append(newlog)
                        self.logEntries.append(newlog)

                    index += 1