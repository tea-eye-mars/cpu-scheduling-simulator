import random
from dataclasses import dataclass, field

@dataclass
class Process:
    pid: int
    arrival_time: int
    burst_time: int
    priority: int
    time_quantum: int
    remaining_time: int = field(init=False)
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0
    response_time: int = -1
    first_execution_time: int = -1

    def __post_init__(self):
        self.remaining_time = self.burst_time

def generate_workload(num_processes: int, max_step: int = 3, max_burst: int = 15):
    """Generates workload with random incremental arrival times, priority, quantum, and burst times."""
    processes = []
    current_time = 0
    for pid in range(1, num_processes + 1):
        current_time += random.randint(0, max_step)
        processes.append(
            Process(
                pid=pid,
                arrival_time=current_time,
                burst_time=random.randint(1, max_burst),
                priority=random.randint(1, 10),
                time_quantum=random.randint(2, 5),
            )
        )
    return processes