import statistics

class SchedulingAgent:
    def __init__(self, processes, A=10, B=5):
        self.processes = [p.copy() for p in processes]
        self.A = A
        self.B = B
        self.quantum_log = []
        self.agent_log = []
        for p in self.processes:
            p["remaining_burst"] = p["burst"]
            p["completion_time"] = None
            p["response_time"] = None  # 🆕 track response time

    def calculate_rank(self, process):
        return self.A * process["burst"] + self.B * process["priority"]

    def compute_dynamic_time_quantum(self):
        ready = [p["remaining_burst"] for p in self.processes if p["remaining_burst"] > 0]
        return int(statistics.median(ready)) if ready else 1

    def sort_processes_by_rank(self, ready_procs):
        return sorted(ready_procs, key=lambda p: self.calculate_rank(p))

    def run(self):
        time = 0
        cycle = 0
        timeline = []
        completed = []

        while any(p["remaining_burst"] > 0 for p in self.processes):
            ready_procs = [p for p in self.processes if p["arrival"] <= time and p["remaining_burst"] > 0]
            if not ready_procs:
                time += 1
                continue

            dtq = self.compute_dynamic_time_quantum()
            ranked = self.sort_processes_by_rank(ready_procs)

            self.quantum_log.append((time, dtq))
            self.agent_log.append({
                "cycle": cycle,
                "start_time": time,
                "dtq": dtq,
                "ranked_pids": [p["pid"] for p in ranked]
            })
            cycle += 1

            for p in ranked:
                if p["arrival"] > time or p["remaining_burst"] == 0:
                    continue

                # 🆕 Set response time only once, on first execution
                if p["response_time"] is None:
                    p["response_time"] = time - p["arrival"]

                exec_time = min(p["remaining_burst"], dtq)
                timeline.append({"pid": p["pid"], "start": time, "end": time + exec_time})
                time += exec_time
                p["remaining_burst"] -= exec_time

                if p["remaining_burst"] == 0:
                    p["completion_time"] = time
                    completed.append({
                        "pid": p["pid"],
                        "end_time": time,
                        "arrival": p["arrival"],
                        "burst": p["burst"],
                        "completion": p["completion_time"],
                        "tat": p["completion_time"] - p["arrival"],
                        "wt": p["completion_time"] - p["arrival"] - p["burst"],
                        "rt": p["response_time"]  # ✅ Add RT
                    })

                break  # run 1 process per cycle like RR

        return timeline, completed, self.quantum_log, self.agent_log
