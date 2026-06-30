class EmailNormalizer:

    @staticmethod
    def normalize(email):

        if not email:
            return None

        return email.strip().lower()