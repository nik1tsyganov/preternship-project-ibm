# Reads in data from CLF file and outputs it like a data stream with timestamp
import time
import random

RANGE = 1000

with open('test_data.txt', 'r') as i:
    with open('new_file.txt', 'a') as o:
        for line in i:
            currentTime = time.strftime('%H:%M:%S:%M')
            o.write(currentTime)
            o.write(' ')
            o.write(line)
            o.flush()
            time.sleep(random.randrange(RANGE)/RANGE)
