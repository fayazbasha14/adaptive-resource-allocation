import sys
import time

job_type = sys.argv[1]  # "CPU" or "MEM"

if job_type == "CPU":
    x = 0
    while True:
        x = x * 1.01 + 1

elif job_type == "MEM":
    data = []
    while True:
        data.extend([0] * 50000)
        time.sleep(0.05)
