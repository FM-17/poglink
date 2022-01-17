import logging
import re
from dataclasses import dataclass, field
from typing import Any, List, Tuple

logger = logging.getLogger(__name__)


class RatesStatus:
    # TODO: Make a to_embed() method similar to what's in RatesDiff but without bolding

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
        logger.debug(f"Splitting rates; expected: {expected}, extras: {extras}")
        return expected, extras

    @classmethod
    def from_raw(cls, raw_txt: str):
        val_dict = cls.parse_raw(raw_txt)

        return cls.from_dict(val_dict)

    @classmethod
    def from_dict(cls, val_dict):
        expected, extras = cls.get_expected_and_extras(val_dict)

        return cls(**expected, **extras)

    def update_vals(self, vals, raw=False):

        parsed_vals = self.parse_raw(vals) if raw else vals

        expected, extras = self.get_expected_and_extras(parsed_vals)

        for k, v in expected.items():
            setattr(self, k, v)

        self.extras.update(extras)

    def to_dict(self, include_extras=False):
        expected, extras = self.get_expected_and_extras(self.__dict__)

        output_dict = expected

        if include_extras:
            output_dict.update(extras)

        return output_dict

    def to_raw(self):
        return "\n".join([f"{k}={v}" for k, v in self.to_dict().items()])

    def get_diff(self, newrates: "RatesStatus"):
        return RatesDiff.from_statuses(self, newrates)

    def to_embed(self):
        rates_dict = self.to_dict(include_extras=False)

        # format embed description
        embed_description = "\n".join(
            [
                "{} × {}".format(re.sub(r"\.0", "", v), self.RATES_NAMES.get(k, k))
                for k, v in rates_dict.items()
            ]
        )

        return embed_description


@dataclass
class RatesDiffItem:
    key: str
    old_val: Any
    new_val: Any
    is_extra: bool = False


@dataclass
class RatesDiff:
    old: RatesStatus = field(default_factory=RatesStatus)
    new: RatesStatus = field(default_factory=RatesStatus)
    items: List[RatesDiffItem] = field(default_factory=list)

    @classmethod
    def from_statuses(cls, old, new):
        old_dict = old.to_dict()
        new_dict = new.to_dict()

        return RatesDiff(
            items=sorted(
                [
                    RatesDiffItem(
                        key=k,
                        old_val=old_dict.get(k),
                        new_val=new_dict.get(k),
                        is_extra=k not in RatesStatus.RATES_NAMES,
                    )
                    for k, _ in set(new_dict.items()) - set(old_dict.items())
                ],
                key=lambda x: x.key,
            ),
            old=old,
            new=new,
        )

    # highlights changed rates in embed
    def to_embed(self):

        rates_dict = self.old.to_dict(include_extras=False)

        # bold updated rates
        updated_rates = {item.key: f"**{item.new_val}**" for item in self.items}

        rates_dict.update(updated_rates)

        # rename keys and format embed description
        embed_description = "\n".join(
            [ 
                "{} × {}".format(re.sub(r"\.0", "", v), self.old.RATES_NAMES.get(k, k))
                for k, v in rates_dict.items()
            ]
        )

        return embed_description
