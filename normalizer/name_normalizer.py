import re

class NameNormalizer:

    @staticmethod
    def normalize(name):
        if not name:
            return None

        name = name.lower().strip()
        name = re.sub(r"[^\w\s]", "", name)   # remove punctuation
        name = re.sub(r"\s+", " ", name)      # collapse spaces

        return name