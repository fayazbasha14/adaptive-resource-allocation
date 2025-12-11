class Allocator:
    def __init__(self, cpu_low=40, mem_high=80):
        self.cpu_low = cpu_low
        self.mem_high = mem_high

    def decide(self, monitor, jobs, sysdata):
        actions = []
        if sysdata["mem"] > self.mem_high:
            run = [j for j in jobs if j["state"] == "RUNNING"]
            if run:
                worst = max(run, key=lambda j: j["mem"])
                job = monitor.find(worst["pid"])
                job.pause()
                actions.append(f"Paused PID {job.pid}")

        if sysdata["cpu"] < self.cpu_low:
            paused = [j for j in jobs if j["state"] == "PAUSED"]
            if paused:
                best = min(paused, key=lambda j: j["mem"])
                job = monitor.find(best["pid"])
                job.resume()
                actions.append(f"Resumed PID {job.pid}")

        return actions
