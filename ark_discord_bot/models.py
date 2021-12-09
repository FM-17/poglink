import datetime
import re
from dataclasses import dataclass, field
from typing import Any, List, Tuple

from dateutil import parser as dateparser
from jinja2 import Template


class RatesStatus:

    RATES_NAMES = {
        "TamingSpeedMultiplier": "Taming",
        "HarvestAmountMultiplier": "Harvesting",
        "XPMultiplier": "XP",
        "MatingIntervalMultiplier": "Mating Interval",
        "BabyMatureSpeedMultiplier": "Maturation",
        "EggHatchSpeedMultiplier": "Hatching",
        "BabyCuddleIntervalMultiplier": "Cuddle Interval",
        "BabyImprintAmountMultiplier": "Imprinting",
        "HexagonRewardMultiplier": "Hexagon Reward",
    }

    def __init__(
        self,
        **kwargs,
    ):
        expected, extras = self.get_expected_and_extras(kwargs)

        for k, v in expected.items():
            setattr(self, k, v)

        self.extras = extras

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__

    @staticmethod
    def parse_raw(raw: str) -> dict:
        parsed_vals = {
            key.strip(): val.strip()
            for key, val in [line.split("=") for line in raw.strip().splitlines()]
        }
        return parsed_vals

    @staticmethod
    def get_expected_and_extras(parsed_vals_dict: dict) -> Tuple[dict, dict]:
        expected = {
            k: v for k, v in parsed_vals_dict.items() if k in RatesStatus.RATES_NAMES
        }
        extras = {
            k: v
            for k, v in parsed_vals_dict.items()
            if k not in RatesStatus.RATES_NAMES and k != "extras"
        }

        if "extras" in parsed_vals_dict:
            extras.update(parsed_vals_dict.get("extras"))

        return expected, extras

    @classmethod
    def from_raw(cls, raw_txt: str):
        val_dict = cls.parse_raw(raw_txt)

        return cls.from_dict(val_dict)

    @classmethod
    def from_dict(cls, val_dict):
        expected, extras = cls.get_expected_and_extras(val_dict)

        return cls(**expected, **extras)

    def update(self, vals, raw=False):

        parsed_vals = self.parse_raw(vals) if raw else vals

        expected, extras = self.get_expected_and_extras(parsed_vals)

        for k, v in expected.items():
            setattr(self, k, v)

        self.extras.update(extras)

    def to_dict(self):
        expected, extras = self.get_expected_and_extras(self.__dict__)

        output_dict = expected
        output_dict.update(extras)

        return output_dict

    def to_raw(self):
        return "\n".join([f"{k}={v}" for k, v in self.to_dict().items()])

    def get_diff(self, newrates: "RatesStatus"):
        old = self.to_dict()
        new = newrates.to_dict()

        return RatesDiff(
            items=sorted(
                [
                    RatesDiffItem(
                        key=k,
                        old=old.get(k),
                        new=new.get(k),
                        extra=k not in RatesStatus.RATES_NAMES,
                    )
                    for k, _ in set(new.items()) - set(old.items())
                ],
                key=lambda x: x.key,
            )
        )


@dataclass
class BansPlatformPair:
    platform: str
    nbans: int

    def to_dict(self):
        return {self.platform: self.nbans}


@dataclass
class BansTimePeriodSummary:
    heading: str
    summary: List[BansPlatformPair]

    def to_dict(self):
        return {self.heading: [s.to_dict() for s in self.summary]}


class BansStatus:
    def __init__(
        self,
        bans: List[BansTimePeriodSummary],
        last_updated: datetime.datetime = None,
    ) -> None:
        self.bans = bans
        self.last_updated = (
            dateparser.parse(last_updated)
            if isinstance(last_updated, str)
            else last_updated
        )

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__

    @staticmethod
    def parse_raw(raw_txt):
        # https://regex101.com/r/KCBt9M/1
        matches = re.findall("(.*)\n(?:=+\n)((?:.+\n)+)", raw_txt)

        parsed_dict = {
            heading: {
                platform.strip(): int(nbans)
                for platform, nbans in [
                    line.split(":") for line in summary.splitlines()
                ]
            }
            for heading, summary in matches
        }

        # TODO: Handle if format ever changes
        date_string = re.search(r"Last Updated: (.*)\s.+", raw_txt).group(1)
        last_updated = dateparser.parse(date_string)
        return parsed_dict, last_updated

    @classmethod
    def from_raw(cls, raw_txt):
        status_dict, last_updated = cls.parse_raw(raw_txt)

        return cls.from_dict(
            {"ban_summaries": status_dict, "last_updated": last_updated}
        )

    def to_dict(self):
        output_dict = {
            "last_updated": self.last_updated.isoformat(),
            "ban_summaries": {
                b.heading: {s.platform: s.nbans for s in b.summary} for b in self.bans
            },
        }
        return output_dict

    def to_raw(self):
        return self.ban_summary_template.render(banstatus=self)

    @classmethod
    def from_dict(cls, d):
        status_dict = d.get("ban_summaries")
        last_updated = d.get("last_updated")
        return cls(
            bans=[
                BansTimePeriodSummary(
                    heading=period,
                    summary=[
                        BansPlatformPair(platform=p, nbans=n)
                        for p, n in summary.items()
                    ],
                )
                for period, summary in status_dict.items()
            ],
            last_updated=last_updated,
        )

    @staticmethod
    def underline(length):
        return "=" * length

    ban_summary_template = Template(
        """{%- for ban_timeperiod in banstatus.bans %}
{{- ban_timeperiod.heading }}
{% for _ in range(ban_timeperiod.heading | length) %}={% endfor %}
{% for ban_summary in ban_timeperiod.summary %}
{{- ban_summary.platform }}: {{ ban_summary.nbans}}
{% endfor %}

{% endfor -%}
Last Updated: {{ banstatus.last_updated.strftime('%d %b %Y %H:%M:%S') }} ET 
"""
    )


@dataclass
class RatesDiffItem:
    key: str
    old: Any
    new: Any
    extra: bool = False


@dataclass
class RatesDiff:
    items: List[RatesDiffItem] = field(default_factory=list)

    # highlights changed rates in embed
    def to_embed(self, rates):

        rates_dict = rates.to_dict()

        # bold updated rates
        updated_rates = {item.key: f"**{item.new}**" for item in self.items}

        rates_dict.update(updated_rates)

        # rename keys and format embed description
        embed_description = "\n".join(
            [
                f"{v.rstrip('.0')} × {rates.RATES_NAMES.get(k,k)}"
                for k, v in rates_dict.items()
            ]
        )

        return embed_description
