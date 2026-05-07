# BMD

BMD (Block Markdown) is a simple markup language that compiles to HTML. A `.bmd` file is made up of named blocks — each block starts with a tag in square brackets and is followed by its content lines.

## File structure

```
[block-type]
content line 1
content line 2
```

Content before the first block tag is invalid and will raise an error.

## Block types

### `[intro]`
Title page. The first line is the document title, subsequent lines are rendered as metadata.

```
[intro]
My Document Title
Author: Jane Smith
Date: 2026-05-06
```

### `[header]`
A section heading.

```
[header]
Introduction
```

### `[p]`
A paragraph. Multiple lines are joined into a single block of text.

```
[p]
This is the first sentence.
This continues the same paragraph.
```

### `[toc]`
Table of contents. Each line is a `title, page` pair.

```
[toc]
Introduction, 1
Methods, 3
Results, 7
```

### `[table]`
A table with a caption. The first line is the caption, followed by rows of cells separated by `---`.

```
[table]
Table 1: Sample data
Name
Age
City
---
Alice
30
London
---
Bob
25
Paris
```

### `[img]`
An image with an optional caption and alt text.

```
[img]
images/chart.png
Figure 1: Growth over time
A bar chart showing growth
```

### `[page-break]`
Inserts a page break. No content lines needed.

```
[page-break]
```

## Usage

```
python -m bmd -i input.bmd -o output.html
```
