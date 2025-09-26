from aadrr import aadrr_scheduler, load_processes

def calculate_metrics(timeline, completed, processes):
    pid_to_proc = {p["pid"]: p for p in processes}

    # 🆕 Track the first start time of each process for RT
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
        rt = first_starts[pid] - arrival  # ✅ RT = first execution - arrival
        results.append((pid, arrival, burst, end, tat, wt, rt))

    # 🖨️ Print header
    print("\nProcess | Arrival | Burst | Completion | TAT | WT | RT")
    for r in results:
        print(f"{r[0]:<8}{r[1]:<9}{r[2]:<7}{r[3]:<12}{r[4]:<5}{r[5]:<4}{r[6]}")

    # 📊 Averages
    avg_tat = sum(r[4] for r in results) / len(results)
    avg_wt = sum(r[5] for r in results) / len(results)
    avg_rt = sum(r[6] for r in results) / len(results)

    print(f"\nAverage TAT: {avg_tat:.2f}")
    print(f"Average WT:  {avg_wt:.2f}")
    print(f"Average RT:  {avg_rt:.2f}")

if __name__ == "__main__":
    procs = load_processes()
    timeline, completed, *_ = aadrr_scheduler(procs)
    calculate_metrics(timeline, completed, procs)
