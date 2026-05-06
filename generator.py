def parse(text: str):
    blocks: list[tuple[str, list[str]]] = []
    current: str | None = None
    lines: list[str] = []

    for index, line in enumerate(text.split("\n")):
        line = line.strip()
        print(f"{line=}\n{current=}")
        if line.startswith("[") and line.endswith("]"):
            if current is not None:
                blocks.append((current, lines))
            current = line[1:-1]
            lines = []
        else:
            if line:
                if not current:
                    raise ValueError(f"Orphaned content found at {index}")
                else:
                    lines.append(line)

    if current is not None:
        blocks.append((current, lines))
    return blocks


def formattedText(text: str) -> str:
    return text


def render_toc(lines: list[str]) -> str:
    output = "<div class='toc-container'>"
    for line in lines:
        print(repr(line))
        title, page = line.split(",")
        output += "<div class='toc'>"
        output += f"<span class='toc-title'>{formattedText(title)}</span>\n"
        output += f"<span class='toc-dots'></span>\n"
        output += f"<span class='toc-page'>{page}</span>"
        output += "</div>"
    output += "</div>"
    return output


def render_header(lines: list[str]) -> str:
    return f"<h2>{formattedText(".".join(lines))}</h2>"


def render_p(lines: list[str]) -> str:
    return f"<p>{formattedText(" ".join(lines))}</p>"


def render_intro(lines: list[str]) -> str:
    title = lines[0]
    meta = "".join(f"<div class='meta'>{line}</div>" for line in lines[1:] if line)
    return f"<div class='title-page'><h1>{title}</h1>{meta}</div>"


def render_table(lines: list[str]) -> str:
    caption = lines[0]
    rows: list[list[str]] = []
    current_row: list[str] = []
    for line in lines[1:]:
        if line == "---":
            if current_row:
                rows.append(current_row)
            current_row = []
        else:
            current_row.append(line)
    if current_row:
        rows.append(current_row)
    header = "".join(f"<th>{cell}</th>" for cell in rows[0])
    body = "".join(
        "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        for row in rows[1:]
    )
    return (
        f"<figure>"
        f"<table>"
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{body}</tbody>"
        f"</table>"
        f"<figcaption>{caption}</figcaption>"
        f"</figure>"
    )


def render_img(lines: list[str]) -> str:
    src = lines[0]
    caption = lines[1] if len(lines) > 1 else ""
    alt = lines[2] if len(lines) > 2 else ""
    return (
        f"<figure>"
        f"<img src='{src}' alt='{alt}'>"
        f"<figcaption>{caption}</figcaption>"
        f"</figure>"
    )


def render_pagebreak(_lines: list[str]) -> str:
    return "<div class='page-break'></div>"


RENDERERS = {
    "intro": render_intro,
    "toc": render_toc,
    "header": render_header,
    "p": render_p,
    "table": render_table,
    "img": render_img,
    "page-break": render_pagebreak,
}


def render(blocks: list[tuple[str, list[str]]]) -> str:
    output: list[str] = []
    with open("header.html", "r") as header:
        HEADER = header.read()
    for block_type, lines in blocks:
        if block_type no in RENDERERS:
            raise ValueError(f"Unkown block type: {block_type}")
        output.append(RENDERERS[block_type](lines))

    return f"{HEADER}<body>{'\n'.join(output)}</body></html>"


if __name__ == "__main__":
    with open("test.bmd", "r") as file:
        blocks = parse(file.read())
        with open("output.html", "w") as output:
            _ = output.write(render(blocks))
