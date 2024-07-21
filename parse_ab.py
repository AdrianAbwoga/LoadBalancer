import matplotlib.pyplot as plt
import re

log_file = 'logs/load_balancing.log'
server_requests = {
    "Server_5001": 0,
    "Server_5002": 0,
    "Server_5003": 0,
    "Server_5004": 0,
    "Server_5005": 0,
    "Server_5006": 0,
}

with open(log_file, 'r') as file:
    logs = file.readlines()

for log in logs:
    match = re.search(r'handled by server ID: (\d+)', log)
    if match:
        server_id = f"Server_{match.group(1)}"
        if server_id in server_requests:
            server_requests[server_id] += 1

servers = list(server_requests.keys())
requests = list(server_requests.values())

plt.bar(servers, requests)
plt.xlabel('Servers')
plt.ylabel('Number of Requests')
plt.title('Request Distribution Across Servers')
plt.show()
