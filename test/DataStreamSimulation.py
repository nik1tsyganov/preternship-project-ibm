# Reads in data from CLF file and outputs it like a data stream with timestamp
import time
import random

RANGE = 1000


def data_stream(mock='mock_data.txt', output='stream_file.txt'):
    with open(mock, 'r') as i:
        with open(output, 'a') as o:
            for line in i:
                currentTime = time.strftime('%H:%M:%S:%M')
                o.write(currentTime)
                o.write(' ')
                o.write(line)
                o.flush()
                time.sleep(random.randrange(RANGE) / RANGE)
