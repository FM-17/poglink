.PHONY: all 
all:

.PHONY: lint 
lint:
	black ark_discord_bot tests

.PHONY: test 
test:
	pytest

.PHONY: clean
clean: clean-python

.PHONY: clean-python 
clean-python:
	rm -rfv dist/*

.PHONY: python-build
python-build: clean-python
	python setup.py sdist

.PHONY: python-publish
python-publish-test: python-build
	scripts/python-publish.sh

.PHONY: python-publish-prod
python-publish-prod: python-build
	PROD=true scripts/python-publish.sh