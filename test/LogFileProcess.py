import sys

sys.path.append('..')
from LogFile import LogFile
from DataStreamSimulation import data_stream
import threading

streamSimulation = threading.Thread(name="Mock Data Stream", target=data_stream, args=('mock_data.txt', 'stream_data.txt'))
streamSimulation.start()


mockLogFile = LogFile("stream_data.txt")
mockLogFile.monitor_file()
