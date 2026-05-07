from bmd.parser import Block


def render_toc(lines: list[str]) -> str:
    output = "<div class='toc-container'>"
    for line in lines:
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
    return f"<h1>{title}</h1>"
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


def render_table_bare(lines: list[str]) -> str:
    rows: list[list[str]] = []
    current_row: list[str] = []
    for line in lines:
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


def render_math(_lines: list[str]) -> str:
    return "<p>MATH UNSUPPORTED</p>"


def render_code(_lines: list[str]) -> str:
    return "<p>CODE UNSUPPORTED</p>"


RENDERERS = {
    "intro": render_intro,
    "toc": render_toc,
    "header": render_header,
    "p": render_p,
    "table": render_table,
    "img": render_img,
    "page-break": render_pagebreak,
    "math": render_math,
    "code": render_code,
}


def formattedText(text: str) -> str:
    return text


def render_engram(blocks: list[Block]) -> str:
    output: list[str] = []
    for block in blocks:
        if block.type not in RENDERERS:
            raise ValueError(f"Unkown block type: {block.type}")
        output.append(RENDERERS[block.type](block.lines))

    return f"<div class='engram-doc'>{'\n'.join(output)}</div>"


def render(blocks: list[Block]) -> str:
    output: list[str] = []
    with open("header.html", "r") as header:
        HEADER = header.read()
    for block in blocks:
        if block.type not in RENDERERS:
            raise ValueError(f"Unkown block type: {block.type}")
        output.append(RENDERERS[block.type](block.lines))

    return f"{HEADER}<body>{'\n'.join(output)}</body></html>"
