from bmd.parser import parse
from bmd.renderer import render, render_engram

class BMDError(Exception):
    """Raised when a .bmd file fails to parse, render, or write."""


def _parse_and_render(input_path: str, renderer):
    try:
        with open(input_path, "r") as f:
            blocks = parse(f.read())
    except FileNotFoundError:
        raise BMDError(f"file not found: {input_path}")
    except ValueError as e:
        raise BMDError(f"invalid BMD in {input_path}: {e}")

    try:
        return renderer(blocks)
    except ValueError as e:
        raise BMDError(f"invalid BMD in {input_path}: {e}")


def _write(output_path: str, html: str) -> None:
    try:
        with open(output_path, "w") as f:
            f.write(html)
    except OSError as e:
        raise BMDError(f"could not write to {output_path}: {e}")


def verify(input_path: str) -> None:
    _parse_and_render(input_path, render)
    print("VERIFIED: OK")


def compile(input_path: str, output_path: str) -> None:
    html = _parse_and_render(input_path, render)
    _write(output_path, html)


def compile_engram(input_path: str, output_path: str) -> None:
    html = _parse_and_render(input_path, render_engram)
    _write(output_path, html)

