from bmd.parser import parse
from bmd.renderer import render


def compile(input_path: str, output_path: str) -> None:
    with open(input_path, "r") as f:
        blocks = parse(f.read())

    html = render(blocks)

    with open(output_path, "w") as f:
        f.write(html)
