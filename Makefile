compile:
	pip install -r requirements.txt

clean:
	rm -rf src/__pycache__
	rm src/*.pyc

run:
	python3 main.py 500 0.2

# Low Iteration Count
# High Max error
scenario-1:
	python3 main.py 100 0.8

# Medium iteration count
# Low Max error
scenario-2:
	python3 main.py 500 0.2

# High Iteration Count
# High Max error
scenario-3:
	python3 main.py 1000 0.8

docker-run:
	docker build -t arl-ai .
	docker run arl-ai
