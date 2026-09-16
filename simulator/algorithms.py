import copy

def simulate_fcfs(processes):
    """First-Come, First-Served (Non-Preemptive)."""
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda p: p.arrival_time)
    current_time, busy_time = 0, 0
    gantt_chart = []

    for p in procs:
        if current_time < p.arrival_time:
            current_time = p.arrival_time
        if p.first_execution_time == -1:
            p.first_execution_time = current_time

        start = current_time
        current_time += p.burst_time
        busy_time += p.burst_time

        p.completion_time = current_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time
        p.response_time = p.first_execution_time - p.arrival_time
        gantt_chart.append((p.pid, start, current_time))

    return procs, current_time, busy_time, gantt_chart


def simulate_srtf(processes):
    """Shortest Remaining Time First (Preemptive SJF)."""
    procs = copy.deepcopy(processes)
    current_time, busy_time, completed = 0, 0, 0
    n = len(procs)
    gantt_chart = []
    current_pid, segment_start = None, 0

    while completed < n:
        ready = [
            p for p in procs if p.arrival_time <= current_time and p.remaining_time > 0
        ]

        if not ready:
            if current_pid is not None:
                gantt_chart.append((current_pid, segment_start, current_time))
                current_pid = None
            current_time += 1
            continue

        ready.sort(key=lambda p: (p.remaining_time, p.arrival_time, p.pid))
        selected = ready[0]

        if current_pid != selected.pid:
            if current_pid is not None:
                gantt_chart.append((current_pid, segment_start, current_time))
            current_pid = selected.pid
            segment_start = current_time

        if selected.first_execution_time == -1:
            selected.first_execution_time = current_time

        selected.remaining_time -= 1
        busy_time += 1
        current_time += 1

        if selected.remaining_time == 0:
            selected.completion_time = current_time
            selected.turnaround_time = selected.completion_time - selected.arrival_time
            selected.waiting_time = selected.turnaround_time - selected.burst_time
            selected.response_time = selected.first_execution_time - selected.arrival_time
            completed += 1
            gantt_chart.append((current_pid, segment_start, current_time))
            current_pid = None

    return procs, current_time, busy_time, gantt_chart


def simulate_rr(processes, default_quantum=3):
    """Round Robin (Preemptive Time Slice)."""
    procs = copy.deepcopy(processes)
    procs.sort(key=lambda p: p.arrival_time)
    current_time, busy_time, completed = 0, 0, 0
    n = len(procs)
    ready_queue, gantt_chart = [], []
    i = 0

    if procs and current_time < procs[0].arrival_time:
        current_time = procs[0].arrival_time

    while i < n and procs[i].arrival_time <= current_time:
        ready_queue.append(procs[i])
        i += 1

    while completed < n:
        if not ready_queue:
            if i < n:
                current_time = procs[i].arrival_time
                while i < n and procs[i].arrival_time <= current_time:
                    ready_queue.append(procs[i])
                    i += 1
            else:
                break

        p = ready_queue.pop(0)
        if p.first_execution_time == -1:
            p.first_execution_time = current_time

        q = p.time_quantum if p.time_quantum > 0 else default_quantum
        exec_time = min(p.remaining_time, q)

        start = current_time
        p.remaining_time -= exec_time
        busy_time += exec_time
        current_time += exec_time
        gantt_chart.append((p.pid, start, current_time))

        while i < n and procs[i].arrival_time <= current_time:
            ready_queue.append(procs[i])
            i += 1

        if p.remaining_time > 0:
            ready_queue.append(p)
        else:
            p.completion_time = current_time
            p.turnaround_time = p.completion_time - p.arrival_time
            p.waiting_time = p.turnaround_time - p.burst_time
            p.response_time = p.first_execution_time - p.arrival_time
            completed += 1

    return procs, current_time, busy_time, gantt_chart