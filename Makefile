venv:
	python3 -m venv .venv
	source .venv/bin/activate

run:
	python3 main.py

coverage:
	pytest --cov=. --cov-fail-under=90 --cov-report=html:report Tests/
	coverage report
	coverage html