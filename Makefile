# Detect OS
UNAME := $(shell uname -s 2>/dev/null || echo Windows_NT)

# Normalize OS name to "Windows_NT" for all Windows environments
ifeq ($(findstring MINGW,$(UNAME)),MINGW)
    OS := Windows_NT
else
    OS := $(UNAME)
endif

# Platform-specific variables
ifeq ($(OS), Windows_NT)
    ACTIVATE = . .venv/Scripts/activate
else
    ACTIVATE = . .venv/bin/activate
endif

# If python is not found, use python3 to create venv
ifeq (, $(shell which python))
    PYTHON_CREATE = python3
else
    PYTHON_CREATE = python
endif

# If pip is not found, use pip3
ifeq (, $(shell which pip))
    PIP = pip3
else
    PIP = pip
endif

venv:
	$(PYTHON_CREATE) -m venv .venv
	$(ACTIVATE)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON_CREATE) main.py

coverage:
	pytest --cov=. --cov-fail-under=90 --cov-report=html:report Tests/
	coverage report
	coverage html