import copy

import pytest

from poglink.models import RatesDiff, RatesDiffItem, RatesStatus, rates


@pytest.fixture()
def sample_rates_txt():
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


@pytest.fixture()
def sample_rates_dict():
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


@pytest.fixture()
def rates_update_txt():
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


@pytest.fixture()
def rates_update_dict():
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


def test_rates_staticmethod_parse_raw(sample_rates_txt):
    d = RatesStatus.parse_raw(sample_rates_txt)

    assert d.get("TamingSpeedMultiplier") == "3.0"
    assert d.get("HexagonRewardMultiplier") == "1.5"


def test_rates_classmethod_from_raw(sample_rates_txt):
    rates = RatesStatus.from_raw(sample_rates_txt)
    assert rates.MatingIntervalMultiplier == "0.6"
    assert rates.BabyCuddleIntervalMultiplier == "0.6"
    assert rates.extras == {"MyMadeUpValue": "69420"}


def test_rates_classmethod_from_dict(sample_rates_dict):
    rates = RatesStatus.from_dict(sample_rates_dict)
    assert rates.MatingIntervalMultiplier == "0.6"
    assert rates.BabyCuddleIntervalMultiplier == "0.6"
    assert rates.extras == {"MyMadeUpValue": "69420"}


def test_rates_method_update_raw(sample_rates_txt, rates_update_txt):
    rates = RatesStatus.from_raw(sample_rates_txt)
    assert rates.XPMultiplier == "3.0"
    assert rates.extras == {"MyMadeUpValue": "69420"}

    rates.update_vals(rates_update_txt, raw=True)

    assert rates.XPMultiplier == "2.0"
    assert rates.extras == {"MyMadeUpValue": "42069", "MyOtherMadeUpValue": "42069"}


def test_rates_method_update_dict(sample_rates_dict, rates_update_dict):
    rates = RatesStatus.from_dict(sample_rates_dict)
    assert rates.XPMultiplier == "3.0"

    rates.update_vals(rates_update_dict, raw=False)

    assert rates.XPMultiplier == "2.0"
    assert rates.extras == {"MyMadeUpValue": "42069", "MyOtherMadeUpValue": "42069"}


def test_rates_staticmethod_get_expected_and_extras(sample_rates_dict):
    expected, extras = RatesStatus.get_expected_and_extras(sample_rates_dict)

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


def test_rates_method_to_raw(sample_rates_dict, sample_rates_txt):
    rates = RatesStatus.from_dict(sample_rates_dict)

    assert (
        rates.to_raw()
        == """\
TamingSpeedMultiplier=3.0
HarvestAmountMultiplier=3.0
XPMultiplier=3.0
MatingIntervalMultiplier=0.6
BabyMatureSpeedMultiplier=3.0
EggHatchSpeedMultiplier=3.0
BabyCuddleIntervalMultiplier=0.6
BabyImprintAmountMultiplier=3.0
HexagonRewardMultiplier=1.5"""
    )


def test_rates_method_to_dict(sample_rates_dict, sample_rates_txt):
    rates = RatesStatus.from_raw(sample_rates_txt)

    assert rates.to_dict() == {
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


def test_rates_method_get_diff(sample_rates_dict):
    rates = RatesStatus.from_dict(sample_rates_dict)

    sample_rates_dict["BabyMatureSpeedMultiplier"] = "4.2"
    sample_rates_dict["CompletelyRandomNewThing"] = "2.2"

    newrates = RatesStatus.from_dict(sample_rates_dict)

    diff = rates.get_diff(newrates)

    assert diff == RatesDiff(
        items=[
            RatesDiffItem(
                key="BabyMatureSpeedMultiplier",
                old_val="3.0",
                new_val="4.2",
                is_extra=False,
            )
        ],
        old=rates,
        new=newrates,
    )

    rates_copy = copy.deepcopy(rates)
    diff = rates.get_diff(rates_copy)

    assert diff == RatesDiff(old=rates, new=rates_copy)


def test_rates_eq(sample_rates_dict, sample_rates_txt):
    rates_from_dict = RatesStatus.from_dict(sample_rates_dict)
    rates_from_txt = RatesStatus.from_raw(sample_rates_txt)

    assert rates_from_dict == rates_from_txt


def test_rates_method_to_embed(sample_rates_dict):
    old_rates = RatesStatus.from_dict(sample_rates_dict)
    sample_rates_dict["XPMultiplier"] = 1.0
    sample_rates_dict["MatingIntervalMultiplier"] = 1.0
    new_rates = RatesStatus.from_dict(sample_rates_dict)

    rates_diff = RatesDiff.from_statuses(old=old_rates, new=new_rates)

    highlighted_embed = """\
3 × Taming
3 × Harvesting
**1** × XP
**1** × Mating Interval
3 × Maturation
3 × Hatching
0.6 × Cuddle Interval
3 × Imprinting
1.5 × Hexagon Reward\
"""
    assert rates_diff.to_embed() == highlighted_embed
