import sys
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BIRTHDAY = date(1991, 7, 14)
WIDTH = 58
CHAR_W = 9.7
LINE_H = 20
PAD = 20

THEMES = {
    "dark": {"bg": "#161b22", "text": "#c9d1d9", "key": "#ffa657", "value": "#a5d6ff", "dots": "#616e7f"},
    "light": {"bg": "#f6f8fa", "text": "#24292f", "key": "#953800", "value": "#0a3069", "dots": "#c2cfde"},
}


def plural(n: int, unit: str) -> str:
    return f"{n} {unit}{'' if n == 1 else 's'}"


def uptime(today: date) -> str:
    years = today.year - BIRTHDAY.year
    months = today.month - BIRTHDAY.month
    days = today.day - BIRTHDAY.day
    if days < 0:
        months -= 1
        prev_month_end = date(today.year, today.month, 1).toordinal() - 1
        days += date.fromordinal(prev_month_end).day
    if months < 0:
        years -= 1
        months += 12
    return f"{plural(years, 'year')}, {plural(months, 'month')}, {plural(days, 'day')}"


def tspan(cls: str, text: str) -> str:
    return f'<tspan class="{cls}">{escape(text)}</tspan>'


def header(title: str) -> str:
    return tspan("text", f"{title} ") + tspan("dots", "-" * (WIDTH - len(title) - 1))


def entry(key: str, value: str) -> str:
    dots = WIDTH - len(key) - len(value) - 3
    if dots < 1:
        raise ValueError(f"Line too long: {key}: {value}")
    return tspan("key", key) + ":" + tspan("dots", " " + "." * dots + " ") + tspan("value", value)


def lines(today: date) -> list[str]:
    return [
        header("sky1407"),
        entry("OS", "Windows 11, Android 16, Linux"),
        entry("Uptime", uptime(today)),
        entry("Host", "Freelancer"),
        entry("Kernel", "Full-Stack Web Developer"),
        entry("IDE", "VSCode 1.141.0"),
        "",
        entry("Languages.Programming", "JavaScript, Python"),
        entry("Languages.Computer", "HTML, CSS, JSON, YAML"),
        entry("Languages.Real", "English, Slovak"),
        "",
        entry("Hobbies.Software", "Android Jailbreaking"),
        entry("Hobbies.Hardware", "Overclocking, Undervolting"),
        "",
        header("- Contact"),
        entry("Email.Personal", "skyjacker007@gmail.com"),
        entry("GitHub", "sky1407"),
    ]


def render(theme: dict, rows: list[str]) -> str:
    width = round(WIDTH * CHAR_W + PAD * 2)
    height = len(rows) * LINE_H + PAD * 2 - 4
    body = "\n".join(
        f'<tspan x="{PAD}" y="{PAD + 14 + i * LINE_H}">{row}</tspan>' for i, row in enumerate(rows) if row
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,'Courier New',monospace" width="{width}px" height="{height}px" font-size="16px">
<style>
.key {{fill: {theme['key']};}}
.value {{fill: {theme['value']};}}
.dots {{fill: {theme['dots']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{width}px" height="{height}px" fill="{theme['bg']}" rx="15"/>
<text fill="{theme['text']}">
{body}
</text>
</svg>
"""


def main() -> int:
    try:
        rows = lines(date.today())
        for name, theme in THEMES.items():
            (ROOT / f"{name}_mode.svg").write_text(render(theme, rows), encoding="utf-8")
    except (OSError, ValueError) as err:
        print(f"Profile generation failed: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
