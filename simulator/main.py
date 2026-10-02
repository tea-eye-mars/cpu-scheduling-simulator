import csv
import os
import random
import matplotlib.pyplot as plt

from process import generate_workload
from algorithms import simulate_fcfs, simulate_srtf, simulate_rr
from metrics import compute_metrics

# ==========================================
# 1. REPORT GENERATION FUNCTIONS
# ==========================================

def run_scaling_experiment():
    """Runs simulation for process counts N = 10, 20, 30, 40, 50."""
    process_counts = [10, 20, 30, 40, 50]
    results = {"FCFS": [], "SRTF": [], "RR": []}

    random.seed(42)  # For reproducible analysis

    for n in process_counts:
        workload = generate_workload(n)

        # FCFS
        fcfs_p, total_t, busy_t, _ = simulate_fcfs(workload)
        results["FCFS"].append(compute_metrics(fcfs_p, total_t, busy_t))

        # SRTF
        srtf_p, total_t, busy_t, _ = simulate_srtf(workload)
        results["SRTF"].append(compute_metrics(srtf_p, total_t, busy_t))

        # Round Robin
        rr_p, total_t, busy_t, _ = simulate_rr(workload)
        results["RR"].append(compute_metrics(rr_p, total_t, busy_t))

    return process_counts, results

def generate_report_plots(process_counts, results):
    """Generates graphs and exports plot image for report inclusion."""
    os.makedirs("report", exist_ok=True) # Added to prevent crash if run before CSV export
    
    metrics = [
        ("avg_wt", "Average Waiting Time (units)", "Waiting Time Comparison"),
        ("avg_tat", "Average Turnaround Time (units)", "Turnaround Time Comparison"),
        ("avg_rt", "Average Response Time (units)", "Response Time Comparison"),
        ("cpu_util", "CPU Utilization (%)", "CPU Utilization Comparison"),
        ("throughput", "Throughput (processes/unit)", "Throughput Comparison"),
    ]

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.flatten()

    for idx, (metric_key, ylabel, title) in enumerate(metrics):
        ax = axes[idx]
        for alg in ["FCFS", "SRTF", "RR"]:
            values = [res[metric_key] for res in results[alg]]
            ax.plot(process_counts, values, marker="o", linewidth=2, label=alg)

        ax.set_title(title, fontsize=12, fontweight="bold")
        ax.set_xlabel("Number of Processes (N)")
        ax.set_ylabel(ylabel)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()

    axes[-1].axis("off")
    plt.tight_layout()
    plt.savefig("report/scheduling_report_results.png", dpi=300)
    print("\n[SUCCESS] Figures saved to 'report/scheduling_report_results.png'")
    plt.show()

def export_to_csv(process_counts, results):
    """Exports simulation results to a CSV file for the report appendix."""
    os.makedirs("report", exist_ok=True)
    filename = "report/simulation_data.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Processes", "Algorithm", "Avg_Waiting_Time", "Avg_Turnaround_Time", 
            "Avg_Response_Time", "CPU_Utilization_%", "Throughput",
        ])

        for idx, n in enumerate(process_counts):
            for alg in ["FCFS", "SRTF", "RR"]:
                m = results[alg][idx]
                writer.writerow([
                    n, alg, 
                    f"{m['avg_wt']:.2f}", f"{m['avg_tat']:.2f}", f"{m['avg_rt']:.2f}", 
                    f"{m['cpu_util']:.2f}", f"{m['throughput']:.4f}"
                ])
    print(f"[SUCCESS] Data exported to '{filename}'")


# ==========================================
# 2. INTERACTIVE SIMULATOR FUNCTIONS
# ==========================================

def print_gantt_chart(gantt_chart):
    """Prints a simple text-based Gantt chart to the console."""
    print("\n--- CPU EXECUTION TIMELINE (GANTT CHART) ---")
    chart_str = "| "
    for pid, start, end in gantt_chart:
        chart_str += f"P{pid} ({start}-{end}) | "
    print(chart_str)
    print("--------------------------------------------\n")

def run_interactive_simulation():
    """Allows the user to select a specific algorithm and process load."""
    print("\n--- SINGLE RUN SIMULATION ---")
    print("Select Algorithm:")
    print("1. First-Come, First-Served (FCFS)")
    print("2. Shortest Remaining Time First (SRTF)")
    print("3. Round Robin (RR)")
    
    algo_choice = input("Enter choice (1-3): ").strip()
    algo_map = {'1': 'FCFS', '2': 'SRTF', '3': 'RR'}
    
    if algo_choice not in algo_map:
        print("Invalid choice. Please enter 1, 2, or 3.")
        return

    try:
        num_processes = int(input("Enter number of processes (e.g., 10, 20, 50): ").strip())
        if num_processes <= 0:
            print("Please enter a positive number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    workload = generate_workload(num_processes)
    algo_name = algo_map[algo_choice]
    
    print(f"\n[Running {algo_name} for {num_processes} processes...]")

    if algo_name == 'FCFS':
        procs, total_t, busy_t, gantt = simulate_fcfs(workload)
    elif algo_name == 'SRTF':
        procs, total_t, busy_t, gantt = simulate_srtf(workload)
    else:
        procs, total_t, busy_t, gantt = simulate_rr(workload)

    metrics = compute_metrics(procs, total_t, busy_t)
    
    print(f"\n=== RESULTS FOR {algo_name} (N={num_processes}) ===")
    print(f"Average Waiting Time    : {metrics['avg_wt']:.2f} units")
    print(f"Average Turnaround Time : {metrics['avg_tat']:.2f} units")
    print(f"Average Response Time   : {metrics['avg_rt']:.2f} units")
    print(f"CPU Utilization         : {metrics['cpu_util']:.2f}%")
    print(f"Throughput              : {metrics['throughput']:.4f} processes/unit")
    
    print_gantt_chart(gantt)


# ==========================================
# 3. MAIN MENU LOOP
# ==========================================

def main_menu():
    """The main interactive loop for the simulator."""
    while True:
        print("\n" + "="*45)
        print("   CPU SCHEDULING SIMULATOR (A/V SYSTEM)")
        print("="*45)
        print("1. Run Single Simulation (Choose Algo & Load)")
        print("2. Run Full Report Experiment (N=10 to 50)")
        print("3. Exit")
        print("="*45)
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == '1':
            run_interactive_simulation()
        elif choice == '2':
            print("\n[INITIATING FULL SCALING EXPERIMENT (N=10 to 50)]")
            counts, metrics_results = run_scaling_experiment()
            generate_report_plots(counts, metrics_results)
            export_to_csv(counts, metrics_results)
            print("[DONE] Check the 'report/' folder for your output files.\n")
        elif choice == '3':
            print("Exiting simulator. Goodbye!")
            break
        else:
            print("Invalid input. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()