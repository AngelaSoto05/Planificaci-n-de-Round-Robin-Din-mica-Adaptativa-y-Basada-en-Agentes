# aadrr.py
import os
import json
from agent import SchedulingAgent

def load_processes(filename="process_data.json"):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)
    with open(full_path, "r") as f:
        return json.load(f)

def aadrr_scheduler(processes):
    agent = SchedulingAgent(processes)
    timeline, completed, quantum_log, agent_log = agent.run()
    return timeline, completed, quantum_log, agent_log

# CLI Test
if __name__ == "__main__":
    processes = load_processes()
    timeline, completed, quantum_log, agent_log = aadrr_scheduler(processes)

    print("\nExecution Timeline:")
    for slot in timeline:
        print(f"{slot['pid']}: {slot['start']} → {slot['end']}")

    print("\n📋 Process Completion Table:")
    for p in completed:
        print(f"{p['pid']} completed at {p['completion']} | TAT={p['tat']} | WT={p['wt']}")

    print("\n🌀 Dynamic Time Quantum Log:")
    for t, q in quantum_log:
        print(f"Time {t}: DTQ = {q}")

    print("\n🤖 Agent Decision Log:")
    for entry in agent_log:
        print(f"Cycle {entry['cycle']} @ {entry['start_time']}: "
              f"DTQ={entry['dtq']} | Ranked: {entry['ranked_pids']}")
