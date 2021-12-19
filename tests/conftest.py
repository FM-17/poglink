import os
import shutil

import pytest

SAMPLE_BANSUMMARY_PATH_1 = "tests/data/bansummary-1.txt"
SAMPLE_BANSUMMARY_PATH_2 = "tests/data/bansummary-2.txt"
LAST_BANSUMMARY_PATH = "tests/data/last_bans.txt"

SAMPLE_DYNAMICCONFIG_PATH_1 = "tests/data/dynamicconfig-1.ini"
SAMPLE_DYNAMICCONFIG_PATH_2 = "tests/data/dynamicconfig-2.ini"
LAST_DYNAMICCONFIG_PATH = "tests/data/last_rates.txt"

# bans
@pytest.fixture
def sample_bansummary_1():
    with open(SAMPLE_BANSUMMARY_PATH_1) as f:
        return f.read()


@pytest.fixture
def sample_bansummary_2():
    with open(SAMPLE_BANSUMMARY_PATH_2) as f:
        return f.read()


@pytest.fixture
def last_bans():
    shutil.copy(SAMPLE_BANSUMMARY_PATH_1, LAST_BANSUMMARY_PATH)
    with open(LAST_BANSUMMARY_PATH) as f:
        yield f.read()
    os.remove(LAST_BANSUMMARY_PATH)


# rates
@pytest.fixture
def sample_dynamicconfig_1():
    with open(SAMPLE_DYNAMICCONFIG_PATH_1) as f:
        return f.read()


@pytest.fixture
def sample_dynamicconfig_2():
    with open(SAMPLE_DYNAMICCONFIG_PATH_2) as f:
        return f.read()


@pytest.fixture
def last_rates():
    shutil.copy(SAMPLE_DYNAMICCONFIG_PATH_1, LAST_DYNAMICCONFIG_PATH)
    with open(LAST_DYNAMICCONFIG_PATH) as f:
        yield f.read()
    os.remove(LAST_DYNAMICCONFIG_PATH)
