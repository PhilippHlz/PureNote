from model.text_style import TextStyle

class ParagraphFormats:
    def __init__(self):
        """
        Repräsentiert eine Sammlung von Absatzformaten, die bei der Textverarbeitung verwendet werden können.
        Die Formate können aktualisiert werden, um den Text einheitlich darzustellen.
        """
        self.style_presets = {
            'p': TextStyle('Arial', 13, False, False, False, False, '#1f2937', 2, 6, 10),
            'h1': TextStyle('Arial', 32, True, False, False, False, '#111827', 1, 26, 14),
            'h2': TextStyle('Arial', 26, True, False, False, False, '#111827', 1, 22, 12),
            'h3': TextStyle('Arial', 22, True, False, False, False, '#111827', 1, 18, 10),
            'h4': TextStyle('Arial', 18, True, False, False, False, '#111827', 1, 14, 8),
            'h5': TextStyle('Arial', 16, True, False, False, False, '#111827', 1, 10, 6),
            'h6': TextStyle('Arial', 14, True, False, False, False, '#374151', 1, 8, 6),
        }
        self.token_map = self._generate_token_map()

    def get_style_preset(self, paragraph_key):
        """
        Ermöglicht es, über einen paragraph_key aus style_presets einen bestimmten TextStyle abzurufen.
        :param paragraph_key: Der Schlüssel des TextStyles, der benötigt wird (p, h1–h6).
        :return: Gibt das zum paragraph_key passende TextStyle-Objekt zurück.
        """
        return self.style_presets[paragraph_key]

    def set_style_preset(self, paragraph_key, text_style):
        """
        Ermöglicht es, über einen paragraph_key aus style_presets einen bestimmten TextStyle zu ersetzen.
        Der Eintrag wird sowohl in style_presets als auch in token_map aktualisiert.
        :param paragraph_key: Der Schlüssel des TextStyles, der ersetzt werden soll (p, h1–h6).
        :param text_style: Das neue TextStyle-Objekt, das eingesetzt werden soll.
        """
        self.style_presets[paragraph_key] = text_style
        self.token_map[paragraph_key] = text_style.generate_token()

    def _generate_token_map(self):
        """
        Generiert eine Map, die aus einem paragraph_key (p, h1–h6) und einem eindeutigen TextStyle-Token besteht.
        Die Tokens werden durch das jeweilige TextStyle-Objekt generiert und setzen sich aus allen Parametern zusammen.
        :return: Eine Map bestehend aus paragraph_key und Token.
        """
        token_map = {}
        for paragraph_key, text_style in self.style_presets.items():
            token_map[paragraph_key] = text_style.generate_token()
        return token_map