from enum import Enum
from utils.types import *

__all__ = [
    "Style"
]

# Does not contain every option--options are added ad-hoc (only as needed)
class ANSICode(Enum):
    RESET = "0"
    # Text Colors
    WHITE = "39"
    PURPLE = "35"
    BLUE = "34"
    YELLOW = "33"
    RED = "31"
    # Styles
    BOLD = "1"
    DIM = "2"
    UNDERLINE = "4"

    def __str__(self) -> str:
        return self.value

    # cant do `__str__` bc `Style`'s `__str__` uses `join`
    def to_seq(self) -> str:
        return "\x1b["+self.value+"m"


class Style:
    def __init__(self, *values: ANSICode):
        self.codes: List[ANSICode] = []
        self.codes.extend(values)

    def __add__(self, other: Union[Self, str]) -> Union[Self, str]:
        if isinstance(other, str):
            return str(self) + other
        else:
            return Style(*(self.codes + other.codes))

    def __add_eq__(self, style: Union[Self, ANSICode]) -> None:
        if isinstance(style, ANSICode):
            self.codes.append(style)
        else:
            self.codes.extend(style.codes)

    def __call__(self, s: str) -> str:
        if len(self.codes) <= 0:
            return s
        else:
            return str(self) + s + str(Style(ANSICode.RESET))

    def substr(self, full: str, sub: str) -> str:
        if len(self.codes) == 0:
            return full
        else:
            return full.replace(sub, self(sub))

    def __str__(self) -> str:
        if len(self.codes) <= 0:
            return ""
        else:
            return "\x1b["+(';'.join([str(code) for code in self.codes]))+"m"


# Add ANSI enum members as members here
for name, enum in ANSICode.__members__.items():
    setattr(Style, name, Style(enum))


### Tests

def test_styles():
    assert str(Style.RESET) == "\x1b[0m"
    assert str(Style.WHITE) == "\x1b[39m"
    assert str(Style.MAGENTA) == "\x1b[35m"
    assert str(Style.BLUE) == "\x1b[34m"
    assert str(Style.YELLOW) == "\x1b[33m"
    assert str(Style.RED) == "\x1b[31m"
    assert str(Style.BOLD) == "\x1b[1m"
    assert str(Style.DIM) == "\x1b[2m"
    assert str(Style.UNDERLINE) == "\x1b[4m"

def test_concat():
    assert str(Style.RED + Style.BOLD) == "\x1b[31;1m"
    assert str(Style.WHITE + Style.DIM + Style.UNDERLINE) == "\x1b[39;2;4m"
    assert str(Style.YELLOW + "test") == "\x1b[33mtest"

def test_concat_eq():
    style = Style.BLUE
    style += Style.UNDERLINE
    style += Style.DIM
    assert str(style) == "\x1b[34;4;2m"

def test_call():
    assert Style.YELLOW("test") == "\x1b[33mtest\x1b[0m"
    style = Style.DIM + Style.BOLD
    assert style("test") == "\x1b[2;1mtest\x1b[0m"
    assert Style()("test") == "test"

def test_substr():
    test_str = "this is a test string"
    assert Style.BLUE.substr(test_str, "test") == "this is a \x1b[34mtest\x1b[0m string"
