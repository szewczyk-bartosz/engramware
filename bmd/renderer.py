from pathlib import Path
import html
from bmd.parser import Block

_HEADER_PATH = Path(__file__).parent.parent / "header.html"

import functools

def strip_lines(fn):
    @functools.wraps(fn)
    def wrapper(lines):
        return fn([line.strip() for line in lines])
    return wrapper

def remove_empty_lines(fn):
    @functools.wraps(fn)
    def wrapper(lines):
        return fn([line for line in lines if line.strip()])
    return wrapper


@strip_lines
@remove_empty_lines
def render_toc(lines: list[str]) -> str:
    output = "<div class='toc-container'>"
    for line in lines:
        if "," not in line:
            raise ValueError(f"toc line must be 'title, page': {line!r}")
        title, page = line.rsplit(",", 1)
        title, page = title.strip(), page.strip()
        output += "<div class='toc'>"
        output += f"<span class='toc-title'>{formattedText(title)}</span>\n"
        output += f"<span class='toc-dots'></span>\n"
        output += f"<span class='toc-page'>{page}</span>"
        output += "</div>"
    output += "</div>"
    return output


@strip_lines
@remove_empty_lines
def render_header(lines: list[str]) -> str:
    return f"<h2>{formattedText(".".join(lines))}</h2>"


@strip_lines
@remove_empty_lines
def render_p(lines: list[str]) -> str:
    return f"<p>{formattedText(" ".join(lines))}</p>"


@strip_lines
@remove_empty_lines
def render_intro(lines: list[str]) -> str:
    title = lines[0]
    return f"<h1>{title}</h1>"
    meta = "".join(f"<div class='meta'>{line}</div>" for line in lines[1:] if line)
    return f"<div class='title-page'><h1>{title}</h1>{meta}</div>"


def _render_table_html(lines: list[str]) -> str:
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
    if not rows:
        raise ValueError("table block requires at least one row of data")
    col_count = len(rows[0])
    if any(len(row) != col_count for row in rows[1:]):
        raise ValueError("table block requires an equal number of columns in each row")
    header = "".join(f"<th>{formattedText(cell)}</th>" for cell in rows[0])
    body = "".join(
        "<tr>" + "".join(f"<td>{formattedText(cell)}</td>" for cell in row) + "</tr>"
        for row in rows[1:]
    )
    return (
        f"<table>"
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{body}</tbody>"
        f"</table>"
    )


@strip_lines
@remove_empty_lines
def render_table(lines: list[str]) -> str:
    if not lines:
        raise ValueError("table block requires a caption")
    caption = lines[0]
    table_html = _render_table_html(lines[1:])
    return (
        f"<figure>"
        f"{table_html}"
        f"<figcaption>{formattedText(caption)}</figcaption>"
        f"</figure>"
    )


@strip_lines
@remove_empty_lines
def render_table_bare(lines: list[str]) -> str:
    table_html = _render_table_html(lines)
    return (
        f"<figure>"
        f"{table_html}"
        f"</figure>"
    )


@strip_lines
@remove_empty_lines
def render_img(lines: list[str]) -> str:
    if not lines:
        raise ValueError("img block requires at least one line (the image path)")
    src = formattedText(lines[0])
    caption = formattedText(lines[1]) if len(lines) > 1 else ""
    alt = formattedText(lines[2]) if len(lines) > 2 else ""
    return (
        f"<figure>"
        f"<img src='{src}' alt='{alt}'>"
        f"<figcaption>{caption}</figcaption>"
        f"</figure>"
    )


@strip_lines
@remove_empty_lines
def render_pagebreak(_lines: list[str]) -> str:
    return "<div class='page-break'></div>"


@strip_lines
@remove_empty_lines
def render_math(lines: list[str]) -> str:
    return f"<div class='math-block' data-latex='{formattedText(" ".join(lines))}'></div>"


def render_code(lines: list[str]) -> str:
    language = lines[0].strip()
    innerHTML = "\n".join([formattedText(i) for i in lines[1:]])
    return f"<pre><code class='language-{language}'>{innerHTML}</code></pre>"
        

@strip_lines
@remove_empty_lines
def render_ul(lines: list[str]) -> str:
    return f"<ul>{"".join([f"<li>{i}</li>" for i in lines])}</ul>"


RENDERERS = {
    "intro": render_intro,
    "toc": render_toc,
    "ul": render_ul,
    "header": render_header,
    "p": render_p,
    "table": render_table,
    "table_bare": render_table_bare,
    "img": render_img,
    "page-break": render_pagebreak,
    "math": render_math,
    "code": render_code,
}


def formattedText(text: str) -> str:
    return html.escape(text);


def render_engram(blocks: list[Block]) -> str:
    output: list[str] = []
    for block in blocks:
        if block.type not in RENDERERS:
            raise ValueError(f"Unkown block type: {block.type}")
        output.append(RENDERERS[block.type](block.lines))

    return f"{'\n'.join(output)}"


def render(blocks: list[Block]) -> str:
    output: list[str] = []
    with open(_HEADER_PATH, "r") as header:
        HEADER = header.read()
    for block in blocks:
        if block.type not in RENDERERS:
            raise ValueError(f"Unkown block type: {block.type}")
        output.append(RENDERERS[block.type](block.lines))

    return f"{HEADER}<body>{'\n'.join(output)}</body></html>"
