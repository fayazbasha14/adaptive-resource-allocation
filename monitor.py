import subprocess
import sys
import time
import psutil
from jobinfo import Job


class Monitor:
    def __init__(self):
        self.jobs = []

    def launch(self, job_type):
        p = subprocess.Popen(
            [sys.executable, "job.py", job_type]
        )
        time.sleep(0.3)

        if psutil.pid_exists(p.pid):
            job = Job(p.pid, job_type)
            self.jobs.append(job)
            print(f"Started {job_type} job PID={p.pid}")
        else:
            print("Process failed!")

    def collect(self):
        data = []
        alive = []

        for job in self.jobs:
            if not psutil.pid_exists(job.pid):
                continue
            data.append(job.snapshot())
            alive.append(job)

        self.jobs = alive

        sys_cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        return data, {"cpu": sys_cpu, "mem": mem.percent}

    def find(self, pid):
        for j in self.jobs:
            if j.pid == pid:
                return j
        return None
