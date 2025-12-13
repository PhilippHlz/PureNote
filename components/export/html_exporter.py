from html import escape


STYLE_TAG_MAPPING = {
    "H1": "h1",
    "H2": "h2",
    "p": "p"
}


def export_editor_to_html(editor, filename="export.html"):
    """
    Exportiert den Inhalt des Tkinter-Editors als HTML-Datei.
    """

    lines = editor.get("1.0", "end-1c").split("\n")

    html_lines = []

    for index, line in enumerate(lines, start=1):
        start_index = f"{index}.0"
        end_index = f"{index}.end"

        tags = editor.tag_names(start_index)

        html_tag = "p"
        for tag in STYLE_TAG_MAPPING:
            if tag in tags:
                html_tag = STYLE_TAG_MAPPING[tag]
                break

        escaped_line = escape(line)

        if "markierung" in tags:
            escaped_line = f"<mark>{escaped_line}</mark>"

        html_lines.append(f"<{html_tag}>{escaped_line}</{html_tag}>")

    html_content = "\n".join(html_lines)

    html = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="utf-8">
    <title>PureNote Export</title>
</head>
<body>
{html_content}
</body>
</html>
"""

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)
