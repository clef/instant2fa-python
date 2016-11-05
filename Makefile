.PHONY: clean-pyc clean-build docs clean
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "watch-test - run tests every time a Python file is saved"
	@echo "coverage - check code coverage quickly with the default Python"
	@echo "docs - generate Sphinx HTML documentation, including API docs"
	@echo "release - package and upload a release to the internal PyPI server"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"
	@echo "develop - bootstrap a development environment"

clean: clean-build clean-pyc clean-test

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -f .coverage
	rm -fr htmlcov/

lint:
	flake8 instant2fa tests

develop: clean
	virtualenv venv
	. venv/bin/activate && pip install -r requirements_dev.txt

test:
	python setup.py test

watch-test: test
	watchmedo shell-command -p '*.py' -c '$(MAKE) test' -R -D .

coverage:
	coverage run --source instant2fa setup.py test
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs:
	rm -f docs/instant2fa.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ instant2fa
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean dist
	twine upload -r clefpypi dist/*

dist: clean
	python setup.py sdist
	ls -l dist

install: clean
	python setup.py install
