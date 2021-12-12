#!/bin/bash

# Try to infer local python package version
PYTHON_PACKAGE_VERSION=$(python3 -c 'from setuptools_scm import get_version; print(get_version(local_scheme="no-local-version"))' || echo 0.0.1.dev0)

# Build docker container
docker build \
    --build-arg "PYTHON_PACKAGE_VERSION=${PYTHON_PACKAGE_VERSION}" \
    -t poglink:latest \
    .
