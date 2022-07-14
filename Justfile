# list all available commands
default:
  just --list

# clean all build, python, and lint files
clean:
	rm -fr build/
	rm -fr docs/_build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr .tox/
	rm -fr .coverage
	rm -fr coverage.xml
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache

# lint, format, and check all files
lint:
	tox -e lint

# run tox / run tests and lint
build:
	tox

# generate Sphinx HTML documentation
generate-docs:
	rm -f docs/swagit_dataset_generator*.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ swagit_dataset_generator **/tests/
	python -msphinx "docs/" "docs/_build/"

# generate Sphinx HTML documentation and serve to browser
serve-docs:
	just generate-docs
	python -mwebbrowser -t file://{{justfile_directory()}}/docs/_build/index.html

# update this repo using latest cookiecutter-py-package
update-from-cookiecutter:
	cookiecutter gh:evamaxfield/cookiecutter-py-package --config-file .cookiecutter.yaml --no-input --overwrite-if-exists --output-dir ..