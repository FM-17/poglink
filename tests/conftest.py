import pytest
import shutil
import os


SAMPLE_BANSUMMARY_PATH = "tests/data/bansummary.txt"
SAMPLE_BANSUMMARY_CHANGED_PATH = "tests/data/bansummary-changed.txt"
LAST_BANSUMMARY_PATH = "tests/data/last_bans.txt"

SAMPLE_DYNAMICCONFIG_PATH = "tests/data/dynamicconfig.ini"
SAMPLE_CHANGED_DYNAMICCONFIG_PATH = "tests/data/dynamicconfig-changed.ini"
LAST_DYNAMICCONFIG_PATH = "tests/data/last_rates.txt"

# bans
@pytest.fixture
def sample_bansummary_txt():
    with open(SAMPLE_BANSUMMARY_PATH) as f:
        return f.read()


@pytest.fixture
def sample_bansummary_changed_ini():
    with open(SAMPLE_BANSUMMARY_CHANGED_PATH) as f:
        return f.read()


@pytest.fixture
def last_bans():
    shutil.copy(SAMPLE_BANSUMMARY_PATH, LAST_BANSUMMARY_PATH)
    with open(LAST_BANSUMMARY_PATH) as f:
        yield f.read()
    os.remove(LAST_BANSUMMARY_PATH)


# rates
@pytest.fixture
def sample_dynamicconfig_ini():
    with open(SAMPLE_DYNAMICCONFIG_PATH) as f:
        return f.read()


@pytest.fixture
def sample_dynamicconfig_changed_ini():
    with open(SAMPLE_CHANGED_DYNAMICCONFIG_PATH) as f:
        return f.read()


@pytest.fixture
def last_rates():
    shutil.copy(SAMPLE_DYNAMICCONFIG_PATH, LAST_DYNAMICCONFIG_PATH)
    with open(LAST_DYNAMICCONFIG_PATH) as f:
        yield f.read()
    os.remove(LAST_DYNAMICCONFIG_PATH)


# http
@pytest.fixture
def configured_httpserver(
    httpserver,
    sample_bansummary_txt,
    sample_dynamicconfig_ini,
):
    httpserver.expect_request("/bansummary.txt").respond_with_data(
        sample_bansummary_txt, content_type="text/plain"
    )
    httpserver.expect_request("/dynamicconfig.ini").respond_with_data(
        sample_dynamicconfig_ini, content_type="text/plain"
    )

    return httpserver