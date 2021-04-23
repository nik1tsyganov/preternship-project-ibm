# Reads in data from CLF file and outputs it like a data stream with timestamp
import time

with open('mock_data.txt', 'r') as i:
    with open('new_file.txt', 'w') as o:
        for line in i:
            currentTime = time.strftime('%H:%M:%S:%M')
            o.write(currentTime)
            o.write(' ')
            o.write(line)
