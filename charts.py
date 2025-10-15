import matplotlib.pyplot as plt
from aadrr import aadrr_scheduler, load_processes
from compare_algorithms import fcfs_scheduler, round_robin_scheduler
def get_avg_metrics(scheduler_func, processes):
    processes_copy = [p.copy() for p in processes]
    timeline, completed, *_  = scheduler_func(processes_copy)
    pid_to_proc = {p["pid"]: p for p in processes}
    
    total_tat, total_wt = 0, 0
    for p in completed:
        pid = p["pid"]
        end = p["end_time"]
        arrival = pid_to_proc[pid]["arrival"]
        burst = pid_to_proc[pid]["burst"]
        tat = end - arrival
        wt = tat - burst
        total_tat += tat
        total_wt += wt

    n = len(processes)
    return round(total_tat / n, 2), round(total_wt / n, 2)

def plot_comparison():
    processes = load_processes()

    # Define the algorithms to compare
    algorithms = {
        "AADRR": aadrr_scheduler,
        "FCFS": fcfs_scheduler,
        "RR": lambda p: round_robin_scheduler(p, time_quantum=4)
    }

    tat_data, wt_data = [], []

    for name, func in algorithms.items():
        tat, wt = get_avg_metrics(func, processes)
        tat_data.append(tat)
        wt_data.append(wt)

    x = list(algorithms.keys())

    # Plotting
    plt.figure(figsize=(12, 5))

    # Turnaround Time
    plt.subplot(1, 2, 1)
    plt.bar(x, tat_data, color='skyblue')
    plt.title("Average Turnaround Time")
    plt.ylabel("Time")
    plt.ylim(0, max(tat_data) + 5)

    # Waiting Time
    plt.subplot(1, 2, 2)
    plt.bar(x, wt_data, color='salmon')
    plt.title("Average Waiting Time")
    plt.ylabel("Time")
    plt.ylim(0, max(wt_data) + 5)

    plt.suptitle("Algorithm Performance Comparison")
    plt.tight_layout()
   #plt.savefig("charts/algorithm_comparison.png")
    plt.savefig("algorithm_comparison.png")
    plt.show()

if __name__ == "__main__":
    plot_comparison()
