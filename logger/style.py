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
        return str(self) + val + str(Style.RESET)

    def __add__(self, other: Union[Self, str]) -> Union[Self, str]:
        if isinstance(other, str):
            return str(self) + other
        else:
            val = Style.BLANK
            val._name_ = self.name + "+" + other.name
            val._value_ = self.value + ";" + other.value
            return val

    def __add_eq__(self, other: Self):
        self._name_ += "+" + other.name
        self._value_ += ";" + other.value

    def substr(self, full: str, sub: str) -> str:
        return full.replace(sub, self(sub))
