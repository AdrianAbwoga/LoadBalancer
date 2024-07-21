
# Load Balancer Performance Analysis

## Overview

This project aims to analyze the performance of a load balancer using ApacheBench (ab) for benchmarking. We perform a series of tests to observe how the load balancer distributes requests among server instances, handles server failures, and scales with an increasing number of server instances. The project includes modifying hash functions to study their impact on load distribution and performance.

## Purpose

The purpose of this project is to:
1. Measure and visualize the performance of a load balancer with varying numbers of server instances.
2. Evaluate the load balancer's ability to handle server failures.
3. Assess the impact of different hash functions on load distribution and performance.

## Installation Instructions

### Prerequisites

- Docker
- Docker Compose
- Python 3.x
- ApacheBench (ab)
- Required Python libraries: `matplotlib`, `pandas`

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/AdrianAbwoga/loadbalancer.git
   cd loadbalancer-performance-analysis
   ```

2. **Build Docker Containers**

   ```bash
   docker-compose build
   ```

3. **Run Docker Containers**

   ```bash
   docker-compose up --scale server=3
   ```

## Usage Guidelines

### Running Benchmarks

1. **Launch 10,000 Async Requests on N=3 Server Containers**

   ```bash
   python3 test1.py
   ```

2. **Parse ApacheBench Output and Visualize**

   ```bash
   python parse_ab.py
   ```

### Tasks and Analysis

#### Task A-1: Load Distribution Analysis

1. **Run the Benchmark**

   ```bash
   python3 test1.py
   ```

2. **Visualize the Data**

   The `parse_ab.py` script will generate bar charts showing "Requests per second" and "Time per request". Use logging or metrics collection in your load balancer to determine the request count handled by each server instance.

#### Task A-2: Scalability Analysis

1. **Increment Server Instances**

  make changes as required by adding servers on by one using the /add end point and run the test1.py for traffic requests to run through followed by the parse_ab.py to visualise.
  
```bash
   curl -X POST -H "Content-Type: application/json" -d '{"hostnames": ["http://localhost:500X"]}' http://localhost:5000/add
   python3 test1.py
   ```

2. **Collect and Visualize Data**

   Parse the output files and create a line chart to show the average load (Requests per second) vs. number of server instances.

#### Task A-3: Fault Tolerance Testing

1. **Test Endpoints**

   Run benchmarks for all your load balancer endpoints (e.g., `/home`, `/about`).

2. **Simulate Server Failure**

   Manually stop one of the server instances to simulate a failure:

   ```bash
   docker stop <container_id>
   ```

3. **Observe Load Balancer Behavior**

   Verify that the load balancer continues to distribute requests to the remaining instances and quickly spawns a new instance if configured.

#### Task A-4: Hash Function Modification

1. **Modify Hash Functions**

   Change the hash functions used in your load balancer implementation.

2. **Run Benchmarks and Compare**

   Repeat the benchmarks from tasks A-1 and A-2 using the new hash functions. Collect and compare the performance data.

## Dependencies

- **Docker**: Containerization platform
- **Docker Compose**: Tool for defining and running multi-container Docker applications
- **Python 3.x**: Programming language
- **ApacheBench (ab)**: Tool for benchmarking
- **Matplotlib**: Python library for creating static, animated, and interactive visualizations
- **Pandas**: Python library for data manipulation and analysis

## Conclusion

This project provides a comprehensive analysis of a load balancer's performance, scalability, and fault tolerance. 

