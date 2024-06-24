from flask import Flask, jsonify, request
from consistent_hash import ConsistentHash
import os
import docker
import requests

app = Flask(__name__)
docker_client = docker.from_env()

# Initialize Consistent Hash
N = 3
hash_map = ConsistentHash(replicas=9, max_slots=512)
for i in range(1, N + 1):
    container_name = f'Server-{i}'
    hash_map.add_node(container_name)

def spawn_container(name):
    docker_client.containers.run(
        'your-server-image-name',
        name=name,
        environment={'SERVER_ID': name},
        ports={'5000/tcp': None},  # map to random port
        detach=True
    )

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        'message': list(hash_map.ring.values()),
        'status': 'successful'
    }), 200

@app.route('/add', methods=['POST'])
def add_replica():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames', [])
    for hostname in hostnames:
        spawn_container(hostname)
        hash_map.add_node(hostname)
    return jsonify({
        'message': 'Replicas added',
        'status': 'successful'
    }), 200

@app.route('/rm', methods=['DELETE'])
def remove_replica():
    data = request.get_json()
    n = data.get('n')
    hostnames = data.get('hostnames', [])
    for hostname in hostnames:
        container = docker_client.containers.get(hostname)
        container.stop()
        container.remove()
        hash_map.remove_node(hostname)
    return jsonify({
        'message': 'Replicas removed',
        'status': 'successful'
    }), 200

@app.route('/<path:path>', methods=['GET'])
def route_request(path):
    node = hash_map.get_node(path)
    if node:
        container = docker_client.containers.get(node)
        port = container.attrs['NetworkSettings']['Ports']['5000/tcp'][0]['HostPort']
        response = requests.get(f'http://localhost:{port}/{path}')
        return response.content, response.status_code
    return jsonify({
        'message': 'No available node',
        'status': 'failure'
    }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
