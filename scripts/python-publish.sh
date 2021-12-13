#!/bin/bash
set -e 

# Unless you explicitly set PROD=true, only publish to the test pypi repo
if ! [ "$PROD" == "true" ]; then
    REPOSITORY_ARGS="--repository testpypi"
fi

# Upload all source distributions in the dist directory.
twine upload $REPOSITORY_ARGS dist/*