.PHONY: build up down test clean

build:
    docker-compose build

up:
    docker-compose up --build --scale server=3

down:
    docker-compose down

test:
    ab -n 10000 -c 100 http://localhost:5000/home > ab_output.txt
    python3 parse_ab.py

clean:
    docker-compose down -v --rmi all --remove-orphans
