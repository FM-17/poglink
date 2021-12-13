import datetime

import pytest

from poglink.models import BansStatus


@pytest.fixture()
def sample_bans_txt():
    return """\
Today's Ban Summary
===================
BattlEye Bans: 2160
PC Bans: 9
Xbox Bans: 4
PS4 Bans: 5


7-Day Ban Summary
==================
BattlEye Bans: 13824
PC Bans: 62
Xbox Bans: 84
PS4 Bans: 109


Lifetime Ban Summary
====================
BattlEye Bans: 34218
PC Bans: 15609
Xbox Bans: 13037
PS4 Bans: 15520


Last Updated: 02 Dec 2021 17:59:03 ET
"""


@pytest.fixture()
def sample_bans_dict():
    return {
        "ban_summaries": {
            "Today's Ban Summary": {
                "BattlEye Bans": 2160,
                "PC Bans": 9,
                "Xbox Bans": 4,
                "PS4 Bans": 5,
            },
            "7-Day Ban Summary": {
                "BattlEye Bans": 13824,
                "PC Bans": 62,
                "Xbox Bans": 84,
                "PS4 Bans": 109,
            },
            "Lifetime Ban Summary": {
                "BattlEye Bans": 34218,
                "PC Bans": 15609,
                "Xbox Bans": 13037,
                "PS4 Bans": 15520,
            },
        },
        "last_updated": "2021-12-02T17:59:03",
    }


def test_parse_raw(sample_bans_txt):
    status_dict, last_updated = BansStatus.parse_raw(sample_bans_txt)

    assert status_dict == {
        "Today's Ban Summary": {
            "BattlEye Bans": 2160,
            "PC Bans": 9,
            "Xbox Bans": 4,
            "PS4 Bans": 5,
        },
        "7-Day Ban Summary": {
            "BattlEye Bans": 13824,
            "PC Bans": 62,
            "Xbox Bans": 84,
            "PS4 Bans": 109,
        },
        "Lifetime Ban Summary": {
            "BattlEye Bans": 34218,
            "PC Bans": 15609,
            "Xbox Bans": 13037,
            "PS4 Bans": 15520,
        },
    }
    assert last_updated == datetime.datetime(
        year=2021, month=12, day=2, hour=17, minute=59, second=3
    )


def test_from_raw_to_dict(sample_bans_txt, sample_bans_dict):
    bans_status = BansStatus.from_raw(sample_bans_txt)
    assert bans_status.to_dict() == sample_bans_dict


def test_from_raw_to_raw(sample_bans_txt):

    bans_status = BansStatus.from_raw(sample_bans_txt)
    bans_status_raw = bans_status.to_raw()
    bans_status_from_raw = BansStatus.from_raw(bans_status_raw)

    assert bans_status == bans_status_from_raw


def test_from_dict_to_dict(sample_bans_dict):
    bans_status = BansStatus.from_dict(sample_bans_dict)

    # Check that date objects are converted properly
    assert bans_status.last_updated == datetime.datetime(
        year=2021, month=12, day=2, hour=17, minute=59, second=3
    )

    # Check that the conversion works in reverse
    assert bans_status.to_dict() == sample_bans_dict
