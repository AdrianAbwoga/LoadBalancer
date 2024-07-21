FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean

ENV SERVER_ID=Server_1

CMD ["python", "app.py"]
