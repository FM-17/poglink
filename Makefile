.PHONY: all 
all: help

## - lint
##	Automatically format project code with black.
.PHONY: lint 
lint:
	black poglink tests

## - test
##	Run pytest tests.
.PHONY: test 
test:
	pytest

## - clean
##	Clean all build directories.
.PHONY: clean
clean: clean-python

## - clean-python
##	Clean python build directory.
.PHONY: clean-python 
clean-python:
	rm -rfv dist/*

## - python-build
##	Build python source distribution (tarball).
.PHONY: python-build
python-build: clean-python
	python setup.py sdist

## - python-publish-test
##	Publish python package to test.pypi.org.
.PHONY: python-publish-test
python-publish-test: python-build
	scripts/python-publish.sh

## - python-publish-prod
##	Publish python package to pypi.org.
.PHONY: python-publish-prod
python-publish-prod: python-build
	PROD=true scripts/python-publish.sh

## - docker-build
##	Build docker image.
.PHONY: docker-build
docker-build:
	scripts/docker-build.sh

## - help:
##	Show this help text.
.PHONY: help
help: 
	@sed -n 's/^##//p' $(MAKEFILE_LIST)