from typing import Any, Tuple, List
from dataclasses import dataclass, field


class RatesStatus:
    DEFAULT_RATES_KEYS = [
        "TamingSpeedMultiplier",
        "HarvestAmountMultiplier",
        "XPMultiplier",
        "MatingIntervalMultiplier",
        "BabyMatureSpeedMultiplier",
        "EggHatchSpeedMultiplier",
        "BabyCuddleIntervalMultiplier",
        "BabyImprintAmountMultiplier",
        "HexagonRewardMultiplier",
    ]

    def __init__(
        self,
        **kwargs,
    ):
        for k in self.DEFAULT_RATES_KEYS:
            setattr(self, k, kwargs.get(k))
            del kwargs[k]

        self.extras = kwargs

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
            k: v
            for k, v in parsed_vals_dict.items()
            if k in RatesStatus.DEFAULT_RATES_KEYS
        }
        extras = {
            k: v
            for k, v in parsed_vals_dict.items()
            if k not in RatesStatus.DEFAULT_RATES_KEYS and k != "extras"
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
                        extra=k not in RatesStatus.DEFAULT_RATES_KEYS,
                    )
                    for k, _ in set(new.items()) - set(old.items())
                ],
                key=lambda x: x.key,
            )
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
