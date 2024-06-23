import re
import matplotlib.pyplot as plt
import pandas as pd

# Function to parse the ab output file
def parse_ab_output(file_path):
    with open(file_path, 'r') as file:
        data = file.read()

    results = {}
    
    # Extracting the required values using regular expressions
    results['Requests per second'] = float(re.search(r"Requests per second:\s+([\d.]+)", data).group(1))
    results['Time per request'] = float(re.search(r"Time per request:\s+([\d.]+)\s+\[ms\] \(mean\)", data).group(1))
    results['Time per request (concurrent)'] = float(re.search(r"Time per request:\s+([\d.]+)\s+\[ms\] \(mean, across all concurrent requests\)", data).group(1))
    results['Transfer rate'] = float(re.search(r"Transfer rate:\s+([\d.]+)\s+\[Kbytes/sec\] received", data).group(1))
    
    # Latency distribution
    latencies = re.findall(r"\s+([\d.]+)%\s+([\d.]+)", data)
    latency_percentiles = {float(percent): float(time) for percent, time in latencies}
    results['Latency Distribution'] = latency_percentiles
    
    return results

# Function to create visualizations
def create_visualizations(results):
    # Plot Requests per second
    plt.figure(figsize=(10, 6))
    plt.bar(['Requests per second'], [results['Requests per second']])
    plt.ylabel('Requests per second')
    plt.title('Requests per second')
    plt.show()
    
    # Plot Time per request
    plt.figure(figsize=(10, 6))
    plt.bar(['Time per request'], [results['Time per request']])
    plt.ylabel('Time per request (ms)')
    plt.title('Time per request')
    plt.show()
    
    # Plot Latency distribution
    latency_df = pd.DataFrame(list(results['Latency Distribution'].items()), columns=['Percentile', 'Latency (ms)'])
    latency_df.plot(x='Percentile', y='Latency (ms)', kind='line', marker='o', figsize=(10, 6))
    plt.title('Latency Distribution')
    plt.xlabel('Percentile')
    plt.ylabel('Latency (ms)')
    plt.grid(True)
    plt.show()

# Main function
def main():
    file_path = 'ab_output.txt'  # Path to your ab output file
    results = parse_ab_output(file_path)
    create_visualizations(results)

if __name__ == "__main__":
    main()
