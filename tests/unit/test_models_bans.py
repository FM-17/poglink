import pytest
import datetime
from ark_discord_bot.models import BansStatus


@pytest.fixture(scope="session")
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
