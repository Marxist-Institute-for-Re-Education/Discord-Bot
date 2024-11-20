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
        if self.is_blank():
            return ""
        else:
            return f"\x1b[{self.value}m"

    def __call__(self, val: str) -> str:
        if self.is_blank():
            return val
        else:
            return str(self) + val + str(Style.RESET)

    def __add__(self, other: Union[Self, str]) -> Union[Self, str]:
        if self.is_blank():
            return other
        elif isinstance(other, str):
            return str(self) + other
        elif other.is_blank():
            return self
        else:
            val = Style.BLANK
            # name only matters for __repr__
            val._name_ = self.name + "+" + other.name
            val._value_ = self._value_ + ";" + other._value_
            return val

    def __add_eq__(self, other: Self):
        if other.is_blank():
            return
        elif self.is_blank():
            self._name_ = other.name
            self._value_ = other._value_
        else:
            self._name_ += "+" + other.name
            self._value_ += ";" + other._value_

    def substr(self, full: str, sub: str) -> str:
        if self.is_blank() or len(sub) == 0:
            return full
        else:
            return full.replace(sub, self(sub))

    def is_blank(self) -> bool:
        return self is Style.BLANK

### Tests

def escape(val: Union[Style, str]):
    s: str = str(val)
    return s.replace("\x1b", "\\x1b")

def test_is_blank():
    assert Style.BLANK.is_blank()
    assert not Style.RED.is_blank()

def test_styles():
    assert str(Style.BLANK) == ""
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
    assert str(Style.BLANK + Style.BOLD) == "\x1b[1m"
    assert str(Style.MAGENTA + Style.BLANK) == "\x1b[35m"
    assert str(Style.Yellow + "test") == "\x1b[33mtest"

def test_concat_eq():
    style = Style.BLUE
    style += Style.UNDERLINE
    style += Style.BLANK
    style += Style.DIM
    assert str(style) == "\x1b[34;4;2m"

def test_call():
    assert Style.YELLOW("test") == "\x1b[33mtest\x1b[0m"
    style = Style.DIM + Style.BOLD
    assert style("test") == "\x1b[2;1mtest\x1b[0m"
    assert Style.BLANK("test") == "test"

def test_substr():
    test_str = "this is a test string"
    assert Style.BLUE.substr(test_str, "test") == "this is a \x1b[34mtest\x1b[0m string"
    assert Style.BLANK.substr(test_str, "test") == test_str
