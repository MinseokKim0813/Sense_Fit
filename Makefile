# If python is not found, use python3 to run the program
ifeq (, $(shell which python))
    PYTHON_CREATE = python3
else
    PYTHON_CREATE = python
endif

run:
	$(PYTHON_CREATE) main.py

coverage:
	pytest --cov=. --cov-fail-under=90 --cov-report=html:report Tests/
	coverage report
	coverage html