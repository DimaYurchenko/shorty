PYTHON_EXECUTABLE ?= venv/bin/python
export PYTHONPATH := $(shell pwd)


create-dev-venv:
	python3 -m venv venv
	make install-requirements
	make install-dev-requirements

create-venv:
	python3 -m venv venv
	make install-requirements

install-dev-requirements:
	${PYTHON_EXECUTABLE} -m pip install --upgrade pip
	${PYTHON_EXECUTABLE} -m pip install -r requirements-dev.txt

install-requirements:
	${PYTHON_EXECUTABLE} -m pip install --upgrade pip
	${PYTHON_EXECUTABLE} -m pip install -r requirements.txt

beautify:
	${PYTHON_EXECUTABLE} -m black app
	${PYTHON_EXECUTABLE} -m isort app

lint:
	${PYTHON_EXECUTABLE} -m pylint app
	${PYTHON_EXECUTABLE} -m black app --check
	${PYTHON_EXECUTABLE} -m isort app --check

run:
	${PYTHON_EXECUTABLE} app/main.py

