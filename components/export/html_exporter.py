from html import escape


STYLE_TAG_MAPPING = {
    "H1": "h1",
    "H2": "h2",
    "p": "p"
}


def export_editor_to_html(editor, filename="export.html"):
    """
    Exportiert den Inhalt des Tkinter-Editors als HTML-Datei.

    Hinweis:
    In unserem Projekt sind die Absatz-/Inline-Stile nicht als "H1/H2/p"-Tags direkt im Text gespeichert,
    sondern als Tokens (z.B. "Arial_13_True_..."), die im editor.token_cache liegen.
    Deshalb wird der paragraph_key aus token_cache gelesen und auf HTML-Tags gemappt.
    """

    lines = editor.get("1.0", "end-1c").split("\n")
    html_lines = []

    for index, line in enumerate(lines, start=1):
        start_index = f"{index}.0"

        tags = editor.tag_names(start_index)

        # Default HTML-Tag
        html_tag = "p"

        # 1) Absatzformat über token_cache bestimmen
        token_tag = None
        if hasattr(editor, "token_cache"):
            for t in tags:
                if t in editor.token_cache:
                    token_tag = t
                    break

        if token_tag:
            paragraph_key = editor.token_cache[token_tag].get("paragraph_key", "p")
            html_tag = STYLE_TAG_MAPPING.get(paragraph_key, "p")

        escaped_line = escape(line)

        # 2) Highlight-Export (ToDo-Highlights oder markierte Bereiche)
        # ToDo-Highlight: Tag ist der ToDo-Titel, Background-Farbe wurde im Editor gesetzt.
        highlight_color = None
        for t in tags:
            if t in ("sel",):
                continue
            if hasattr(editor, "token_cache") and t in editor.token_cache:
                continue

            # Wenn der Tag eine Hintergrundfarbe hat, exportieren wir als mark
            try:
                bg = editor.tag_cget(t, "background")
                if bg:
                    highlight_color = bg
                    break
            except Exception:
                pass

        if highlight_color:
            escaped_line = f'<mark style="background-color: {highlight_color};">{escaped_line}</mark>'

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
