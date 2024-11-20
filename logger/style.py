from enum import Enum
from utils import Union, Self


# Does not contain every option--options are added ad-hoc (only as needed)
class Style(Enum):
    BLANK = ""
    RESET = "0"
    # Text Colors
    WHITE = "39"
    MAGENTA = "35"
    BLUE = "34"
    YELLOW = "33"
    RED = "31"
    # Styles
    BOLD = "1"
    DIM = "2"
    UNDERLINE = "4"

    def __str__(self) -> str:
        if self.value == "":
            return ""
        else:
            return f"\x1b[{self.value}m"

    def __call__(self, val: str) -> str:
        if self.is_blank():
            return val
        else:
            return str(self) + val + str(Style.RESET)

    def __add__(self, other: Union[Self, str]) -> Union[Self, str]:
        if isinstance(other, str):
            return str(self) + other
        elif self.is_blank():
            return other
        elif other.is_blank():
            return self
        else:
            val = Style.BLANK
            # name only matters for __repr__
            val._name_ = self.name + "+" + other.name
            val._value_ = self.value + ";" + other.value
            return val

    def __add_eq__(self, other: Self):
        if other.is_blank():
            return
        elif self.is_blank():
            self._name_ = other.name
            self._value_ = other.value
        else:
            self._name_ += "+" + other.name
            self._value_ += ";" + other.value

    def substr(self, full: str, sub: str) -> str:
        if self.is_blank() or len(sub) == 0:
            return full
        else:
            return full.replace(sub, self(sub))

    def is_blank(self) -> bool:
        return self.value == ""
