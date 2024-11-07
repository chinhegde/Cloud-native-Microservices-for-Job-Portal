import re
import matplotlib.pyplot as plt

# Define function to parse ab output and extract metrics
def parse_ab_output(file_path):
    with open(file_path, 'r') as file:
        output = file.read()

    metrics = {}
    requests_per_second_match = re.search(r'Requests per second:\s*([\d.]+)', output)
    latency_match = re.search(r'Time per request:\s*([\d.]+)\s*ms\s*\(mean\)', output)
    throughput_match = re.search(r'Transfer rate:\s*([\d.]+)\s*[\w/]+', output)
   
    if requests_per_second_match:
        metrics['Requests per Second'] = float(requests_per_second_match.group(1))
    if latency_match:
        metrics['Latency'] = float(latency_match.group(1))
    if throughput_match:
        metrics['Throughput'] = float(throughput_match.group(1))
   
    return metrics

# Define file paths for each test
file_paths = {
    'Single Instance': 'ab_bench_single_instances.txt',
    'Two Instances': 'ab_bench_two_instances.txt',
    'Three Instances': 'ab_bench_3_instances.txt'
}

# Collect metrics from each file
results = {}
for config, file_path in file_paths.items():
    metrics = parse_ab_output(file_path)
    results[config] = metrics

# Plotting
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
metrics_names = list(results['Single Instance'].keys())

for i, metric_name in enumerate(metrics_names):
    values = [results[config][metric_name] for config in file_paths.keys()]
    if metric_name == 'Latency':
        # Latency is plotted differently (lower values are better)
        axs[i].bar(file_paths.keys(), values, color='red')
    else:
        axs[i].bar(file_paths.keys(), values)
    axs[i].set_title(metric_name)
    axs[i].set_xlabel('Configuration')
    axs[i].set_ylabel(metric_name)

plt.tight_layout()
plt.show()