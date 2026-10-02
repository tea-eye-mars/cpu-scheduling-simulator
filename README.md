```markdown
# CPU Scheduling Simulator for Audio-Video Systems

This project is a custom-built, discrete-event CPU scheduling simulator developed in Python. It evaluates the performance of three core scheduling algorithms—**First-Come, First-Served (FCFS)**, **Shortest Remaining Time First (SRTF)**, and **Round Robin (RR)**—specifically within the context of soft real-time Audio and Video processing systems.

## 🧠 How It Works

In a multimedia operating system, the CPU acts as a single processing pipeline handling vastly different tasks. Audio processes (like sound playback) are typically short and require instantaneous CPU time to prevent stuttering. Video processes (like encoding) are massive and CPU-heavy. 

This simulator tests how different algorithms handle a mixed workload scaling from $N = 10$ to $50$ processes:
* **FCFS (Non-preemptive):** Tasks run until completion. Demonstrates the "Convoy Effect" where short audio tasks get stuck waiting behind large video renders.
* **SRTF (Preemptive):** The CPU dynamically switches to the task with the shortest remaining time. Mathematically minimizes average waiting time but risks starving longer video processes.
* **Round Robin (Preemptive):** Uses a time quantum to cycle through tasks. Guarantees fast, predictable response times, making it the ideal choice for continuous A/V playback.

The simulator tracks and averages five key OS metrics: **Waiting Time**, **Turnaround Time**, **Response Time**, **CPU Utilization**, and **Throughput**.

## ⚙️ Prerequisites

To run this project on your local machine, you will need:
* **Python 3.x** installed and added to your system `PATH`.
* **Git** (to clone the repository).
* The **Matplotlib** library (for rendering the performance graphs).

## 🚀 Setup and Installation

**1. Clone the repository:**
Open your terminal (Command Prompt, Git Bash, or PowerShell) and run:
```bash
git clone [https://github.com/YOUR-USERNAME/cpu-scheduling-simulator.git](https://github.com/YOUR-USERNAME/cpu-scheduling-simulator.git)
cd cpu-scheduling-simulator

```

*(Note: Replace `YOUR-USERNAME` with your actual GitHub username).*

**2. Install dependencies:**
Install the required graphing library using Python's package manager:

```bash
python -m pip install matplotlib

```

*(Troubleshooting: If you are on Windows and `python` is not recognized, try running `py -m pip install matplotlib` instead).*

## 💻 How to Run the Simulator

The simulator features an interactive Command Line Interface (CLI). Launch it from the root directory of the project:

```bash
python simulator/main.py

```

*(Or `py simulator/main.py` on Windows).*

### Main Menu Options:

* **Option 1: Run Single Simulation**
Allows you to manually select an algorithm (FCFS, SRTF, or RR) and input a specific number of processes. The terminal will output the raw performance metrics and generate a custom **text-based Gantt Chart** showing the exact CPU execution timeline (demonstrating preemption and queueing).
* **Option 2: Run Full Report Experiment**
Automates the exact experiment parameters outlined in the project brief. It scales workloads from $N = 10, 20, 30, 40$, to $50$ processes (using a fixed random seed for reproducible data).
* It exports a compiled data table to `report/simulation_data.csv`.
* It renders a 3x2 grid of line graphs visualizing the performance comparisons and saves it to `report/scheduling_report_results.png`.


* **Option 3: Exit**
Safely terminates the application.

## 📂 Project Directory Structure

* `simulator/`
* `main.py`: The entry point, housing the CLI menu and automation scripts.
* `algorithms.py`: Contains the deep-copy simulation logic for FCFS, SRTF, and RR.
* `process.py`: Defines the `Process` data class and the random workload generator.
* `metrics.py`: Handles the mathematical calculation of WT, TAT, RT, Utilization, and Throughput.


* `report/`: Contains the final IMRAD formatted research report (`.md`/`.pdf`), alongside the generated CSV data and PNG graphs.
* `presentation/`: Contains the PowerPoint slide deck and methodology flowchart.