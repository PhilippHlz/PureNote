import random

class Task:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.color = self._generate_random_color()

    @staticmethod
    def _generate_random_color():
        letters = "0123456789ABCDEF"
        color = "#"
        for i in range(6):
            color += random.choice(letters)
        return color