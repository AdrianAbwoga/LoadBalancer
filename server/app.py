from flask import Flask, jsonify, request
import os
import logging

app = Flask(__name__)

# Configure logging
log_path = '/logs/load_balancing.log'
os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')

@app.route('/home', methods=['GET'])
def home():
    server_id = os.getenv('SERVER_ID', 'Unknown')
    # Log each request
    logging.info(f"Request served by: {server_id}")
    return jsonify({
        "message": f"Hello from Server: {server_id}",
        "status": "successful"
    }), 200

@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
