FROM python:3.9-slim

# Copy server code
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run server
CMD ["python", "server.py"]
