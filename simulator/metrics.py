def compute_metrics(procs, total_time, busy_time):
    """Calculates all required operating system performance metrics."""
    n = len(procs)
    avg_tat = sum(p.turnaround_time for p in procs) / n
    avg_wt = sum(p.waiting_time for p in procs) / n
    avg_rt = sum(p.response_time for p in procs) / n
    cpu_util = (busy_time / total_time) * 100 if total_time > 0 else 0
    throughput = n / total_time if total_time > 0 else 0

    return {
        "avg_tat": avg_tat,
        "avg_wt": avg_wt,
        "avg_rt": avg_rt,
        "cpu_util": cpu_util,
        "throughput": throughput,
    }