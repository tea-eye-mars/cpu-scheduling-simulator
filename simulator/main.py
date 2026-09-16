import random
import matplotlib.pyplot as plt

from process import generate_workload
from algorithms import simulate_fcfs, simulate_srtf, simulate_rr
from metrics import compute_metrics


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


if __name__ == "__main__":
    counts, metrics_results = run_scaling_experiment()

    print("=== CPU SCHEDULING SIMULATION RESULTS SUMMARY ===")
    for idx, n in enumerate(counts):
        print(f"\n--- Process Count: {n} ---")
        for alg in ["FCFS", "SRTF", "RR"]:
            m = metrics_results[alg][idx]
            print(
                f"{alg:5s} | WT: {m['avg_wt']:.2f} | TAT: {m['avg_tat']:.2f} | "
                f"RT: {m['avg_rt']:.2f} | Util: {m['cpu_util']:.1f}% | TP: {m['throughput']:.3f}"
            )

    generate_report_plots(counts, metrics_results)