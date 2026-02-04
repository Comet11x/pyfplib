SHELL = /bin/bash
PYVERSION = 3.14
PWD = $(shell pwd)
ROOT_DIR = $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PKG_NAME = pyfplib
BIN_DIR = $(ROOT_DIR)/bin
SRC_DIR = $(ROOT_DIR)/src/$(PKG_NAME)
PKG_DIR = $(SRC_DIR)
MAIN_FILE = pyfplib.py
ENTRY_POINT = $(SRC_DIR)/$(MAIN_FILE)
TEST_DIR = $(ROOT_DIR)/tests
EXCLUDED_TEST_DIRS = $(TEST_DIR)/excluded
COVERAGE_REPORT_HTML = coverage_html
VENV_FILE = .venv
VENV_SUFFIX = _venv
VENV_DEFAULT_NAME = $(PKG_NAME)$(VENV_SUFFIX)
VENV_NAME := $(shell test -s $(VENV_FILE) && cat $(VENV_FILE) || echo $(VENV_DEFAULT_NAME))
VENV_DIR = $(ROOT_DIR)/$(VENV_NAME)
VENV_ACTIVATE = $(VENV_DIR)/bin/activate 
DEV_REQUIREMENT = $(ROOT_DIR)/requirements/dev.txt
PROD_REQUIREMENT = $(ROOT_DIR)/requirements.txt
EXCLUDED_DIRS = 

run_flake8:
	source $(VENV_ACTIVATE) && PYTHONPATH=$(ROOT_DIR) flake8 --exclude=$(EXCLUDED_DIRS) tests $(PKG_DIR)

run_pylint:
	source $(VENV_ACTIVATE) && PYTHONPATH=$(ROOT_DIR) pylint --output-format=colorized  $(PKG_DIR)

run_black:
	source $(VENV_ACTIVATE) && PYTHONPATH=$(ROOT_DIR) black --check $(TEST_DIR) $(PKG_DIR)

run_lint: run_flake8 run_black run_pylint

run_type_checking:
	source $(VENV_ACTIVATE) && PYTHONPATH=$(ROOT_DIR) mypy --python-version=$(PYVERSION) $(SRC_DIR)

run_tests:
	source $(VENV_ACTIVATE) && MODE="UNIT" PYTHONPATH=$(ROOT_DIR) pytest -s -v $(TEST_DIR)/$(FILE) --ignore=$(EXCLUDED_TEST_DIRS)

watch_test_files:
	source $(VENV_ACTIVATE) && MODE="UNIT" PYTHONPATH=$(ROOT_DIR) $(PYTHON) ./bin/watch_test_files.py

show_coverage:
	source $(VENV_ACTIVATE) && PYTHONPATH=$(ROOT_DIR) pytest --cov=$(PKG_NAME) --cov-report term-missing

show_coverage_as_html:
	source $(VENV_ACTIVATE) &&  PYTHONPATH=$(ROOT_DIR) pytest --cov=$(PKG_NAME) --cov-report=html
	rm -rf $(COVERAGE_REPORT_HTML)
	mv htmlcov $(COVERAGE_REPORT_HTML)
	cd $(COVERAGE_REPORT_HTML) && $(PYTHON) -m http.server 0

install_virtualenv:
	$(PYTHON) -m pip install virtualenv

--make_virtualenv: install_virtualenv
	if [[ ! -d $(VENV_DIR) ]]; then \
		virtualenv $(VENV_NAME);    \
	fi

install_dev_requirements: --make_virtualenv
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r $(DEV_REQUIREMENT)

run_checks:
	black --check $(SRC_DIR)
	flake8 $(SRC_DIR)
	mypy $(SRC_DIR)
	ruff check $(SRC_DIR)
	CUDA_VISIBLE_DEVICES='' pytest -v --color=yes --doctest-modules $(TEST_DIR) $(SRC_DIR)
