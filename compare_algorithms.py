from aadrr import aadrr_scheduler, load_processes
from metrics import calculate_metrics
from typing import Callable

# ----------------- FCFS -----------------
def fcfs_scheduler(processes):
    processes = sorted(processes, key=lambda x: x["arrival"])
    time, timeline, completed = 0, [], []
    first_start = {}

    for p in processes:
        if time < p["arrival"]:
            time = p["arrival"]
        start = time
        end = start + p["burst"]
        if p["pid"] not in first_start:
            first_start[p["pid"]] = start
        timeline.append({"pid": p["pid"], "start": start, "end": end})
        completed.append({"pid": p["pid"], "end_time": end})
        time = end

    return timeline, completed

# ----------------- Round Robin -----------------
def round_robin_scheduler(processes, time_quantum=4):
    from collections import deque
    processes = [p.copy() for p in sorted(processes, key=lambda x: x["arrival"])]
    queue = deque()
    timeline, completed = [], []
    time = 0
    arrived = []
    first_start = {}

    while processes or queue or arrived:
        arrived += [p for p in processes if p["arrival"] <= time]
        processes = [p for p in processes if p["arrival"] > time]
        for p in arrived:
            if p not in queue:
                queue.append(p)
        arrived = []

        if not queue:
            time += 1
            continue

        p = queue.popleft()
        pid = p["pid"]
        exec_time = min(time_quantum, p["burst"])

        if pid not in first_start:
            first_start[pid] = time

        timeline.append({"pid": pid, "start": time, "end": time + exec_time})
        time += exec_time
        p["burst"] -= exec_time

        if p["burst"] > 0:
            queue.append(p)
        else:
            completed.append({"pid": pid, "end_time": time})

    return timeline, completed

# ----------------- Unified Metrics Printer -----------------
def print_metrics(timeline, completed, processes, algo_name):
    pid_to_proc = {p["pid"]: p for p in processes}
    first_starts = {}
    for slot in timeline:
        pid = slot["pid"]
        if pid not in first_starts:
            first_starts[pid] = slot["start"]

    results = []

    for p in completed:
        pid = p["pid"]
        end = p["end_time"]
        arrival = pid_to_proc[pid]["arrival"]
        burst = pid_to_proc[pid]["burst"]
        tat = end - arrival
        wt = tat - burst
        rt = first_starts[pid] - arrival  # ✅ RT = first start - arrival
        results.append((pid, arrival, burst, end, tat, wt, rt))

    print(f"\n=== {algo_name} Scheduler ===")
    print("Process | Arrival | Burst | Completion | TAT  | WT   | RT")
    for r in results:
        print(f"{r[0]:<8}{r[1]:<9}{r[2]:<7}{r[3]:<12}{r[4]:<6}{r[5]:<6}{r[6]}")

    avg_tat = round(sum(r[4] for r in results) / len(results), 2)
    avg_wt = round(sum(r[5] for r in results) / len(results), 2)
    avg_rt = round(sum(r[6] for r in results) / len(results), 2)

    print(f"\nAverage TAT: {avg_tat}")
    print(f"Average WT:  {avg_wt}")
    print(f"Average RT:  {avg_rt}")

    return avg_tat, avg_wt, avg_rt

# ----------------- Runner -----------------
def run_and_compare():
    algorithms: dict[str, Callable] = {
        "AADRR": aadrr_scheduler,
        "FCFS": fcfs_scheduler,
        "RR": lambda p: round_robin_scheduler(p, time_quantum=4),
    }

    comparison = []

    for name, scheduler in algorithms.items():
        procs = load_processes()
        timeline, completed, *_ = scheduler(procs)
        avg_tat, avg_wt, avg_rt = print_metrics(timeline, completed, procs, name)
        comparison.append((name, avg_tat, avg_wt, avg_rt))

    print("\n===== Scheduling Comparison =====")
    print("Algorithm    | Avg TAT | Avg WT | Avg RT")
    print("-------------|---------|--------|--------")
    for name, tat, wt, rt in comparison:
        print(f"{name:<13}| {tat:<8}| {wt:<7}| {rt}")

    best = min(comparison, key=lambda x: (x[1], x[2], x[3]))  # prioritize TAT, then WT, then RT
    print(f"\n✅ {best[0]} yields the best overall average TAT, WT, and RT.")

if __name__ == "__main__":
    run_and_compare()
