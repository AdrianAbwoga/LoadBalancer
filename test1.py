import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def send_request(i):
    response = requests.get(f'http://localhost:5000/some_path_{i}')
    return response.json()

def main():
    num_requests = 10000  # Adjust as needed
    max_workers = 50  # Number of threads to use

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request, i) for i in range(num_requests)]
        
        for future in as_completed(futures):
            try:
                data = future.result()
                print(data)
            except Exception as e:
                print(f"Request generated an exception: {e}")

if __name__ == "__main__":
    main()
