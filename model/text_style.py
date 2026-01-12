class TextStyle:
    """
    Repräsentiert einen TextStyle bzw. Schriftstil mit allen notwendigen Parametern.
    """

    def __init__(self, family, size, bold, italic, underline, highlight, color, line_height, space_before, space_after):
        self.family = family
        self.size = size
        self.bold = bold
        self.italic = italic
        self.underline = underline
        self.highlight = highlight
        self.color = color
        self.line_height = line_height
        self.space_before = space_before
        self.space_after = space_after

    def generate_token(self):
        """
        Generiert einen individuellen Token anhand der übergebenen Parameter.
        :return: Ein Token, der aus allen Parametern besteht.
        """
        safe_family = self.family.replace(' ', '_')
        return f"{safe_family}_{self.size}_{self.bold}_{self.italic}_{self.underline}_{self.highlight}_{self.color}_{self.line_height}_{self.space_before}_{self.space_after}"
