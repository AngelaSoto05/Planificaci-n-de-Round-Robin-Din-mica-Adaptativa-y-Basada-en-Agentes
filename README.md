# AADRR Scheduling Algorithm Simulation

**Author:**  
M.Tech Microproject - Advanced Operating Systems  
Python 3.11.9  
IDE: VS Code  
Platform: Windows 10/11  

---

## 📁 Project Structure

```plaintext
aadrr_project/
├── agent.py                  # 🔁 Agent-based scheduling logic (AADRR)
├── aadrr.py                  # Scheduler wrapper, uses SchedulingAgent
├── compare_algorithms.py     # FCFS, RR, AADRR comparison logic
├── metrics.py                # Metrics calculations (TAT, WT) [optional]
├── charts.py                 # Plots avg TAT/WT comparison as bar chart
├── visualize.py              # Gantt chart generation (matplotlib)
├── process_data.json         # 🔢 Sample process input (used for CLI testing)
├── requirements.txt          # 📦 All Python dependencies
├── README.md                 # 📘 Project documentation
├── aadrr_thesis_report.docx  # 📄 Your final M.Tech report (optional)
├── presentation.pptx         # 🎓 Final viva / review presentation (optional)

└── app/                      # 🌐 Flask web application
    ├── app.py               # Main Flask routes: input + result views
    ├── static/
    │   └── gantt_chart.png  # 🖼️ Saved Gantt chart image
    └── templates/
        ├── home.html        # 🏠 Input form page
        └── result.html      # 📊 Results display and comparison page




## Description

AADRR (Agent-Based Adaptive Dynamic Round Robin) is an advanced process scheduling algorithm that improves over classic Round Robin by:

🧮 Dynamic Time Quantum (DTQ): Uses the median burst time for fair time slicing.

📊 Process Ranking: Combines burst time and priority to sort processes each round.

⏱️ Improved Performance: Reduces turnaround and waiting time.

This project simulates the AADRR logic, visualizes execution using Gantt charts, and compares it against traditional algorithms like FCFS.

## How to Run

1. Install Python (v3.11+ recommended)

2. Create and activate a virtual environment (optional but recommended)

3. Install dependencies - pip install -r requirements.txt

4. Run the main scheduler - python aadrr.py

5. View performance metrics - python metrics.py

6. Comparison - python compare_algorithms.py

7. View Gantt chart - python visualize.py

8. Generate performance bar charts - python charts.py


9. Launch Flask UI - 
cd app
python app.py
Then open your browser