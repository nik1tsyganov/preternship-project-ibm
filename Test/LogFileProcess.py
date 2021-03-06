import sys
sys.path.append('..')
from LogFile import LogFile
from Utilities import data_stream
import threading

#streamSimulation = threading.Thread(name="Mock Data Stream", target=data_stream, args=('../Data/sysstat_all.log',
#                                                                                       'stream_data.txt'))
#streamSimulation.start()


def handle_data(logEntries, errorLogs, warningLogs):
    #print(list(map(lambda x: x.data, logEntries)))
    #print(list(map(lambda x: x.data, warningLogs)))
    for qa in errorLogs:
        print(qa.data.strip("\n"))


mockLogFile = LogFile("../Data/qa-1080ti-003.log")
mockLogFile.monitor_file(handle_data)
