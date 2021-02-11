import time
import sys

name = sys.argv[1]

for i in range(int(sys.argv[2])):
    print(name, i)
    time.sleep(1)
