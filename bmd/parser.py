from dataclasses import dataclass


@dataclass
class Block:
    type: str
    lines: list[str]


def parse(text: str) -> list[Block]:
    blocks: list[Block] = []
    current: str | None = None
    lines: list[str] = []

    for index, line in enumerate(text.split("\n")):
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            if current is not None:
                blocks.append(Block(current, lines))
            current = line[1:-1]
            lines = []
        else:
            if not line:
                continue
            if current is None:
                raise ValueError(f"Orphaned content found at {index}")
            lines.append(line)

    # Last block needs manual adding
    if current is not None:
        blocks.append(Block(current, lines))
    return blocks
