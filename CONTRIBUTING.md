# Contributing

## Initial Setup
1. Install python3.7 (optional: Set up virtual environment)
2. Install development requirements: `python3 -m pip install -r requirements.dev.txt`
3. (Optional, but recommended) Set up [pre-commit](https://pre-commit.com/) to automatically validate code before it can be committed.
    - Automatically install the pre-commit script in `.git`: `pre-commit install` 
    - Run once manually in order to fetch all required packages and validate existing code: `pre-commit run --all`


## Style
- Code is to be formatted according to [Black](https://github.com/psf/black). 
    - Run `make lint-check` to check code for formatting errors.
    - Run `make lint` to check code ***and automatically fix*** any formatting errors.
- Imports should be ordered according to [isort](https://github.com/PyCQA/isort).
    - Run `make isort-check` to check code for import misordering.
    - Run `make isort` to check code ***and automatically fix*** any import misordering.
