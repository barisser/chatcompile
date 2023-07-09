

build:
	. venv/bin/activate && pip-compile -o requirements.txt reqs.in && pip install -r requirements.txt