import datetime
import re
from dataclasses import dataclass
from typing import List

from dateutil import parser as dateparser
from jinja2 import Template


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

{% endfor -%}items: List[RatesDiffItem] = field(default_factory=list)
Last Updated: {{ banstatus.last_updated.strftime('%d %b %Y %H:%M:%S') }} ET 
"""
    )
