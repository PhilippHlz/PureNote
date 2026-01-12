from tkinter.filedialog import asksaveasfilename
from tkinter import *
from tkinter import messagebox
from html import escape

# Mapping von internen Absatzformat-Keys auf die entsprechenden HTML-Tags
STYLE_TAG_MAPPING = {
    "p": "p",
    "h1": "h1",
    "h2": "h2",
    "h3": "h3",
    "h4": "h4",
    "h5": "h5",
    "h6": "h6",
}

# Kapselt die komplette Logik für den HTML-Export als eigenes Frame-Widget.
class HtmlExporter(Frame):
    def __init__(self, parent, editor):
        # Parent-Frame initialisieren und Referenz auf den Editor speichern
        super().__init__(master=parent)
        self.editor = editor
        # Button für den Export
        self.export_button = Button(self, text="HTML Exportieren", command=self.export)
        self.export_button.pack(fill="x")
        self.pack(fill="x", pady=(25, 0))
        
 # Öffnet einen Speichern-Dialog und schreibt den generierten HTML-Code in eine Datei.
    def export(self):
        file_path = asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML-Dateien", "*.html")],
            title="HTML Export speichern"
        )
 # Abbruch, wenn der Dialog ohne Auswahl geschlossen wird
        if not file_path:
            return

        html = self._build_html()

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html)

        messagebox.showinfo("Export", "HTML Export erfolgreich gespeichert.")

 # Baut den vollständigen HTML-String aus dem Inhalt und den Tags des Editors.
    def _build_html(self):
        lines = self.editor.get("1.0", "end-1c").split("\n")
        html_lines = []

        for index, line in enumerate(lines, start=1):
            start_index = f"{index}.0"
            tags = self.editor.tag_names(start_index)

 # Absatzformat aus den Tags bestimmen (p, h1–h6)
            paragraph_tag = self._get_paragraph_tag(tags)
 # Text für HTML escapen  
            escaped_text = escape(line)

 # Optionales Highlight (ToDo-Markierungen etc.) als <mark>-Tag exportieren
            highlight_style = self._get_highlight(tags)
            if highlight_style:
                escaped_text = f'<mark style="background-color:{highlight_style};">{escaped_text}</mark>'

            html_lines.append(f"<{paragraph_tag}>{escaped_text}</{paragraph_tag}>")

        html_content = "\n".join(html_lines)

        return f"""<!DOCTYPE html>
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

     # Ermittelt anhand der Token-Tags das passende HTML-Tag für den Absatz.
    def _get_paragraph_tag(self, tags):
     # Stil-Tags aus dem Token-Cache ignorieren
        if not hasattr(self.editor, "token_cache"):
            return "p"

        for t in tags:
            if t in self.editor.token_cache:
                key = self.editor.token_cache[t].get("paragraph_key", "p")
                key = key.lower()
                return STYLE_TAG_MAPPING.get(key, "p")

        return "p"

    # Prüft, ob für die aktuelle Zeile ein Hintergrund-Tag gesetzt ist.
    # Gibt ggf. die Hintergrundfarbe zurück, die als <mark>-Style verwendet wird.
    def _get_highlight(self, tags):
        for t in tags:
            if hasattr(self.editor, "token_cache") and t in self.editor.token_cache:
                continue
             # Selektionstag ignorieren
            if t == "sel":
                continue

            try:
                bg = self.editor.tag_cget(t, "background")
                if bg:
                    return bg
            except Exception:
                pass

        return None
