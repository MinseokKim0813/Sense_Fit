venv:
	python3 -m venv .venv
	source .venv/bin/activate

run:
	python3 main.py

coverage:
	pytest --cov=. --cov-fail-under=80 --cov-report=html:report Tests/
