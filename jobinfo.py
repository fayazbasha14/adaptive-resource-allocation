import psutil


class Job:
    def __init__(self, pid, job_type):
        self.pid = pid
        self.proc = psutil.Process(pid)
        self.type = job_type
        self.state = "RUNNING"

    def snapshot(self):
        try:
            return {
                "pid": self.pid,
                "type": self.type,
                "cpu": self.proc.cpu_percent(),
                "mem": self.proc.memory_info().rss / (1024 * 1024),
                "state": self.state
            }
        except psutil.NoSuchProcess:
            self.state = "TERM"
            return None

    def pause(self):
        self.proc.suspend()
        self.state = "PAUSED"

    def resume(self):
        self.proc.resume()
        self.state = "RUNNING"
