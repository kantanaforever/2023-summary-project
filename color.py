"""ANSI color codes
used for UX
"""

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"


def colorise(color: str, text: str) -> str:
    return color + text + END

def black(text: str) -> str:
    return colorise(BLACK, text)

def red(text: str) -> str:
    return colorise(RED, text)

def green(text: str) -> str:
    return colorise(GREEN, text)

def brown(text: str) -> str:
    return colorise(BROWN, text)

def blue(text: str) -> str:
    return colorise(GREEN, text)

def purple(text: str) -> str:
    return colorise(PURPLE, text)

def cyan(text: str) -> str:
    return colorise(CYAN, text)

def light_gray(text: str) -> str:
    return colorise(LIGHT_GRAY, text)

def dark_gray(text: str) -> str:
    return colorise(DARK_GRAY, text)

def light_red(text: str) -> str:
    return colorise(LIGHT_RED, text)

def light_green(text: str) -> str:
    return colorise(LIGHT_GREEN, text)

def yellow(text: str) -> str:
    return colorise(YELLOW, text)

def light_blue(text: str) -> str:
    return colorise(LIGHT_BLUE, text)

def light_purple(text: str) -> str:
    return colorise(LIGHT_PURPLE, text)

def light_cyan(text: str) -> str:
    return colorise(LIGHT_CYAN, text)

def light_white(text: str) -> str:
    return colorise(LIGHT_WHITE, text)

def bold(text: str) -> str:
    return colorise(BOLD, text)

def faint(text: str) -> str:
    return colorise(FAINT, text)

def italic(text: str) -> str:
    return colorise(ITALIC, text)

def underline(text: str) -> str:
    return colorise(UNDERLINE, text)

def blink(text: str) -> str:
    return colorise(BLINK, text)

def negative(text: str) -> str:
    return colorise(NEGATIVE, text)

def crossed(text: str) -> str:
    return colorise(CROSSED, text)
