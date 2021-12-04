import pytest
import copy
from ark_discord_bot.models import RatesStatus


@pytest.fixture(scope="session")
def sample_bans_txt():
    return """\
TamingSpeedMultiplier=3.0
HarvestAmountMultiplier=3.0
XPMultiplier=3.0
MatingIntervalMultiplier=0.6
BabyMatureSpeedMultiplier=3.0
EggHatchSpeedMultiplier=3.0
BabyCuddleIntervalMultiplier=0.6
BabyImprintAmountMultiplier=3.0
HexagonRewardMultiplier=1.5
MyMadeUpValue=69420"""


@pytest.fixture(scope="session")
def sample_bans_dict():
    return {
        "TamingSpeedMultiplier": "3.0",
        "HarvestAmountMultiplier": "3.0",
        "XPMultiplier": "3.0",
        "MatingIntervalMultiplier": "0.6",
        "BabyMatureSpeedMultiplier": "3.0",
        "EggHatchSpeedMultiplier": "3.0",
        "BabyCuddleIntervalMultiplier": "0.6",
        "BabyImprintAmountMultiplier": "3.0",
        "HexagonRewardMultiplier": "1.5",
        "MyMadeUpValue": "69420",
    }


@pytest.fixture(scope="session")
def bans_update_txt():
    return """\
TamingSpeedMultiplier=2.0
HarvestAmountMultiplier=2.0
XPMultiplier=2.0
MatingIntervalMultiplier=0.3
BabyMatureSpeedMultiplier=2.0
EggHatchSpeedMultiplier=2.0
BabyCuddleIntervalMultiplier=0.3
BabyImprintAmountMultiplier=2.0
HexagonRewardMultiplier=1.9
MyMadeUpValue=42069
MyOtherMadeUpValue=42069"""


@pytest.fixture(scope="session")
def bans_update_dict():
    return {
        "TamingSpeedMultiplier": "2.0",
        "HarvestAmountMultiplier": "2.0",
        "XPMultiplier": "2.0",
        "MatingIntervalMultiplier": "0.3",
        "BabyMatureSpeedMultiplier": "2.0",
        "EggHatchSpeedMultiplier": "2.0",
        "BabyCuddleIntervalMultiplier": "0.3",
        "BabyImprintAmountMultiplier": "2.0",
        "HexagonRewardMultiplier": "1.9",
        "MyMadeUpValue": "42069",
        "MyOtherMadeUpValue": "42069",
    }


def test_parse_rates(sample_bans_txt):
    d = RatesStatus.parse_raw(sample_bans_txt)

    assert d.get("TamingSpeedMultiplier") == "3.0"
    assert d.get("HexagonRewardMultiplier") == "1.5"


def test_from_raw(sample_bans_txt):
    rates = RatesStatus.from_raw(sample_bans_txt)
    assert rates.MatingIntervalMultiplier == "0.6"
    assert rates.BabyCuddleIntervalMultiplier == "0.6"
    assert rates.extras == {"MyMadeUpValue": "69420"}


def test_from_dict(sample_bans_dict):
    rates = RatesStatus.from_dict(sample_bans_dict)
    assert rates.MatingIntervalMultiplier == "0.6"
    assert rates.BabyCuddleIntervalMultiplier == "0.6"
    assert rates.extras == {"MyMadeUpValue": "69420"}


def test_update_from_raw(sample_bans_txt, bans_update_txt):
    rates = RatesStatus.from_raw(sample_bans_txt)
    assert rates.XPMultiplier == "3.0"
    assert rates.extras == {"MyMadeUpValue": "69420"}

    rates.update(bans_update_txt, raw=True)

    assert rates.XPMultiplier == "2.0"
    assert rates.extras == {"MyMadeUpValue": "42069", "MyOtherMadeUpValue": "42069"}


def test_update_from_dict(sample_bans_dict, bans_update_dict):
    rates = RatesStatus.from_dict(sample_bans_dict)
    assert rates.XPMultiplier == "3.0"

    rates.update(bans_update_dict, raw=False)

    assert rates.XPMultiplier == "2.0"
    assert rates.extras == {"MyMadeUpValue": "42069", "MyOtherMadeUpValue": "42069"}


def test_get_expected_and_extras(sample_bans_dict):
    expected, extras = RatesStatus.get_expected_and_extras(sample_bans_dict)

    assert expected == {
        "TamingSpeedMultiplier": "3.0",
        "HarvestAmountMultiplier": "3.0",
        "XPMultiplier": "3.0",
        "MatingIntervalMultiplier": "0.6",
        "BabyMatureSpeedMultiplier": "3.0",
        "EggHatchSpeedMultiplier": "3.0",
        "BabyCuddleIntervalMultiplier": "0.6",
        "BabyImprintAmountMultiplier": "3.0",
        "HexagonRewardMultiplier": "1.5",
    }

    assert extras == {
        "MyMadeUpValue": "69420",
    }


def test_to_raw(sample_bans_dict, sample_bans_txt):
    rates = RatesStatus.from_dict(sample_bans_dict)

    assert rates.to_raw() == sample_bans_txt


def test_to_dict(sample_bans_dict, sample_bans_txt):
    rates = RatesStatus.from_raw(sample_bans_txt)

    assert rates.to_dict() == sample_bans_dict


def test_get_diff(sample_bans_dict):
    rates = RatesStatus.from_dict(sample_bans_dict)

    sample_bans_dict["BabyMatureSpeedMultiplier"] = "4.2"
    sample_bans_dict["CompletelyRandomNewThing"] = "2.2"

    newrates = RatesStatus.from_dict(sample_bans_dict)

    diff = rates.get_diff(newrates)

    assert diff == {
        "BabyMatureSpeedMultiplier": {"old": "3.0", "new": "4.2", "extra": False},
        "CompletelyRandomNewThing": {"old": None, "new": "2.2", "extra": True},
    }

    rates_copy = copy.deepcopy(rates)
    diff = rates.get_diff(rates_copy)

    assert diff == {}
