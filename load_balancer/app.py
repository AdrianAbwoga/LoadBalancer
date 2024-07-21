from flask import Flask, request, jsonify
from consistent_hashing import ConsistentHashing
import logging
import os

app = Flask(__name__)

# Configure logging
log_path = '/logs/load_balancing.log'
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')

# Initialize load balancer with default settings
lb = ConsistentHashing(num_slots=512, num_virtual_servers=100)

@app.route('/rep', methods=['GET'])
def get_replicas():
    replicas = lb.get_replicas()
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": replicas
        },
        "status": "successful"
    }), 200

@app.route('/add', methods=['POST'])
def add_servers():
    data = request.json
    hostnames = data.get("hostnames", [])
    
    for hostname in hostnames:
        lb.add_server(hostname)
    
    return jsonify({
        "message": {
            "N": len(lb.get_replicas()),
            "replicas": lb.get_replicas()
        },
        "status": "successful"
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_servers():
    data = request.json
    hostnames = data.get("hostnames", [])
    
    for hostname in hostnames:
        lb.remove_server(hostname)
    
    return jsonify({
        "message": {
            "N": len(lb.get_replicas()),
            "replicas": lb.get_replicas()
        },
        "status": "successful"
    }), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    server_url = lb.get_server_url(path)
    if server_url:
        server_id = server_url.split(':')[2]  # Assuming server_url format is http://localhost:500X
        logging.info(f"Request routed to: {server_url} for path: {path}, handled by server ID: {server_id}")
        return jsonify({"message": f"Redirected to {server_url}"}), 200
    else:
        logging.error(f"Request failed for path: {path} - No server found")
        return jsonify({
            "message": "<Error> '/other' endpoint does not exist in server replicas",
            "status": "failure"
        }), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
