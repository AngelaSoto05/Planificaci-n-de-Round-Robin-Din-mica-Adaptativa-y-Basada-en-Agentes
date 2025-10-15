import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for web
import matplotlib.pyplot as plt
import os
import numpy as np
from aadrr import aadrr_scheduler, load_processes

def generate_gantt_chart(timeline, filename="app/static/gantt_chart.png"):
    if not timeline:
        print("⚠️ Empty timeline! Cannot draw Gantt chart.")
        return

    timeline = sorted(timeline, key=lambda x: x["start"])
    fig, ax = plt.subplots(figsize=(10, 3))

    y_labels = sorted(set(p['pid'] for p in timeline))
    y_map = {pid: i for i, pid in enumerate(y_labels)}

    for slot in timeline:
        ax.broken_barh(
            [(slot['start'], slot['end'] - slot['start'])],
            (y_map[slot['pid']] * 10, 9),
            facecolors='tab:blue'
        )
        ax.text(
            slot['start'] + 0.5,
            y_map[slot['pid']] * 10 + 4,
            slot['pid'],
            va='center',
            ha='left',
            color='white',
            fontsize=8
        )

    ax.set_yticks([i * 10 + 4 for i in range(len(y_labels))])
    ax.set_yticklabels(y_labels)
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart")
    ax.grid(True)

    dir_path = os.path.dirname(filename)
    if dir_path:
        os.makedirs(dir_path, exist_ok=True)

    plt.tight_layout()
    plt.savefig(filename)
    print(f"✅ Gantt chart saved at: {os.path.abspath(filename)}")
    plt.close()

def visualize_timeline(timeline):
    fig, gnt = plt.subplots()
    gnt.set_title("AADRR Gantt Chart")
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Processes")

    pids = sorted(set(p["pid"] for p in timeline))
    y_ticks = [10 * (i + 1) for i in range(len(pids))]
    gnt.set_yticks(y_ticks)
    gnt.set_yticklabels(pids)
    gnt.grid(True)

    pid_map = {pid: y for pid, y in zip(pids, y_ticks)}
    colors = ['skyblue', 'lightgreen', 'salmon', 'gold']

    for i, slot in enumerate(timeline):
        gnt.broken_barh(
            [(slot['start'], slot['end'] - slot['start'])],
            (pid_map[slot['pid']], 9),
            facecolors=colors[i % len(colors)]
        )

    plt.tight_layout()
    #plt.show()
    plt.savefig('mi_grafica.png')  # Guarda como PNG
    plt.savefig('mi_grafica.pdf')  # Guarda como PDF
    plt.close()   

def generate_comparison_chart(all_results, filename="app/static/comparison_chart.png"):
    algorithms = list(all_results.keys())
    avg_tats = [all_results[algo]["avg_tat"] for algo in algorithms]
    avg_wts = [all_results[algo]["avg_wt"] for algo in algorithms]
    avg_rts = [all_results[algo]["avg_rt"] for algo in algorithms]

    x = np.arange(len(algorithms))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width, avg_tats, width=width, label="Avg TAT", color='#42a5f5')
    ax.bar(x, avg_wts, width=width, label="Avg WT", color='#66bb6a')
    ax.bar(x + width, avg_rts, width=width, label="Avg RT", color='#ffa726')

    ax.set_xlabel("Scheduling Algorithm", fontsize=12)
    ax.set_ylabel("Average Time", fontsize=12)
    ax.set_title("📊 Comparison of TAT, WT, and RT Across Algorithms", fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()
    ax.grid(axis='y', linestyle="--", alpha=0.6)

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"✅ Comparison chart saved at: {os.path.abspath(filename)}")
    plt.close()

if __name__ == "__main__":
    procs = load_processes()
    timeline, *_ = aadrr_scheduler(procs)
    visualize_timeline(timeline)
