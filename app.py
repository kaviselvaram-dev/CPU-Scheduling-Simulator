from flask import Flask, render_template, request
import copy

app = Flask(__name__)

# ---------- Helper Functions ----------
def make_instruction(name, arrival, burst, priority=0):
    # Safely handle empty inputs
    arrival = int(arrival) if str(arrival).strip().isdigit() else 0
    burst = int(burst) if str(burst).strip().isdigit() else 0
    priority = int(priority) if str(priority).strip().isdigit() else 0

    return {
        "name": name,
        "arrival": arrival,
        "burst": burst,
        "priority": priority,
        "remaining": burst,
        "start": None,
        "finish": None
    }

def calculate_results(instructions):
    results = []
    total_tat, total_wait = 0, 0
    for ins in instructions:
        tat = ins["finish"] - ins["arrival"]
        wait = tat - ins["burst"]
        results.append({
            **ins,
            "tat": tat,
            "wait": wait
        })
        total_tat += tat
        total_wait += wait
    n = len(instructions)
    if n == 0:
        return [], 0, 0
    avg_tat = round(total_tat / n, 2)
    avg_wait = round(total_wait / n, 2)
    return results, avg_tat, avg_wait

# ---------- Scheduling Algorithms ----------
def fcfs(ins):
    ins = sorted(copy.deepcopy(ins), key=lambda x: x["arrival"])
    time = 0
    for i in ins:
        if time < i["arrival"]:
            time = i["arrival"]
        i["start"] = time
        time += i["burst"]
        i["finish"] = time
    return ins

def sjf(ins):
    ins = copy.deepcopy(ins)
    time = 0
    completed = []
    while ins:
        ready = [i for i in ins if i["arrival"] <= time]
        if not ready:
            time += 1
            continue
        current = min(ready, key=lambda x: x["burst"])
        current["start"] = time
        time += current["burst"]
        current["finish"] = time
        completed.append(current)
        ins.remove(current)
    return completed

def srtf(ins):
    ins = copy.deepcopy(ins)
    time = 0
    completed = []
    while ins:
        ready = [i for i in ins if i["arrival"] <= time]
        if not ready:
            time += 1
            continue
        current = min(ready, key=lambda x: x["remaining"])
        if current["start"] is None:
            current["start"] = time
        current["remaining"] -= 1
        time += 1
        if current["remaining"] == 0:
            current["finish"] = time
            completed.append(current)
            ins.remove(current)
    return completed

def priority_non_preemptive(ins):
    ins = copy.deepcopy(ins)
    time = 0
    completed = []
    while ins:
        ready = [i for i in ins if i["arrival"] <= time]
        if not ready:
            time += 1
            continue
        current = min(ready, key=lambda x: x["priority"])
        current["start"] = time
        time += current["burst"]
        current["finish"] = time
        completed.append(current)
        ins.remove(current)
    return completed

def priority_preemptive(ins):
    ins = copy.deepcopy(ins)
    time = 0
    completed = []
    while ins:
        ready = [i for i in ins if i["arrival"] <= time]
        if not ready:
            time += 1
            continue
        # Choose process with highest priority (lowest number)
        current = min(ready, key=lambda x: x["priority"])
        if current["start"] is None:
            current["start"] = time
        current["remaining"] -= 1
        time += 1
        if current["remaining"] == 0:
            current["finish"] = time
            completed.append(current)
            ins.remove(current)
    return completed

def round_robin(ins, quantum=2):
    ins = sorted(copy.deepcopy(ins), key=lambda x: x["arrival"])
    queue = []
    time = 0
    completed = []
    while ins or queue:
        while ins and ins[0]["arrival"] <= time:
            queue.append(ins.pop(0))
        if not queue:
            time += 1
            continue
        current = queue.pop(0)
        if current["start"] is None:
            current["start"] = time
        run_time = min(quantum, current["remaining"])
        current["remaining"] -= run_time
        time += run_time
        while ins and ins[0]["arrival"] <= time:
            queue.append(ins.pop(0))
        if current["remaining"] > 0:
            queue.append(current)
        else:
            current["finish"] = time
            completed.append(current)
    return completed

# ---------- Flask Routes ----------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    algo = request.form.get('algorithm', 'FCFS')
    data = request.form.getlist('process')
    quantum = int(request.form.get('quantum', 2))

    processes = []
    for d in data:
        if not d or not d.strip():
            continue
        parts = d.split(',')
        if len(parts) < 3:
            continue
        n, a, b, *p = parts
        p = p[0] if p else 0
        processes.append(make_instruction(n.strip(), a.strip(), b.strip(), p))

    if algo == 'FCFS':
        result = fcfs(processes)
    elif algo == 'SJF':
        result = sjf(processes)
    elif algo == 'SRTF':
        result = srtf(processes)
    elif algo == 'Priority (Non-Preemptive)':
        result = priority_non_preemptive(processes)
    elif algo == 'Priority (Preemptive)':
        result = priority_preemptive(processes)
    elif algo == 'Round Robin':
        result = round_robin(processes, quantum)
    else:
        result = processes

    results, avg_tat, avg_wait = calculate_results(result)

    gantt_data = [
        {"Task": ins["name"], "Start": ins["start"], "Finish": ins["finish"]}
        for ins in result
    ]

    return render_template(
        'results.html',
        algo=algo,
        results=results,
        avg_tat=avg_tat,
        avg_wait=avg_wait,
        gantt_data=gantt_data
    )

if __name__ == '__main__':
    app.run(debug=True, port=5002)
