class CandidateMatcher:
    """
    Determines whether two candidate records
    belong to the same person using a
    deterministic matching strategy.
    """

    @staticmethod
    def email_match(candidate1: dict, candidate2: dict):
        email1 = candidate1.get("email")
        email2 = candidate2.get("email")

        return (
            email1 is not None
            and email2 is not None
            and email1 == email2
        )

    @staticmethod
    def phone_match(candidate1: dict, candidate2: dict):
        phone1 = candidate1.get("phone")
        phone2 = candidate2.get("phone")

        return (
            phone1 is not None
            and phone2 is not None
            and phone1 == phone2
        )

    @staticmethod
    def name_match(candidate1: dict, candidate2: dict):
        name1 = candidate1.get("full_name")
        name2 = candidate2.get("full_name")

        return (
            name1 is not None
            and name2 is not None
            and name1 == name2
        )

    @classmethod
    def match(cls, candidate1: dict, candidate2: dict):
        """
        Matching priority:
        1. Email
        2. Phone
        3. Full Name (fallback)

        Returns:
            (matched: bool, reason: str)
        """

        if cls.email_match(candidate1, candidate2):
            return True, "Matched by Email"

        if cls.phone_match(candidate1, candidate2):
            return True, "Matched by Phone"

        if cls.name_match(candidate1, candidate2):
            return True, "Matched by Full Name"

        return False, "No Match"