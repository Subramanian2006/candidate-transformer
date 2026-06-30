class EmailNormalizer:

    @staticmethod
    def normalize(email):
        if not isinstance(email, str):
            return None


        if not email:
            return None

        return email.strip().lower()
