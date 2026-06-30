from normalizer.name_normalizer import NameNormalizer
from normalizer.email_normalizer import EmailNormalizer
from normalizer.phone_normalizer import PhoneNormalizer
from normalizer.skill_normalizer import SkillNormalizer


class CandidateNormalizer:
    """
    Applies all available field normalizers
    to a candidate dictionary.
    """

    @staticmethod
    def normalize(candidate: dict):

        if not candidate:
            return {}

        normalized = candidate.copy()

        # Name
        if "full_name" in normalized:
            normalized["full_name"] = NameNormalizer.normalize(
                normalized["full_name"]
            )

        # Email
        if "email" in normalized:
            normalized["email"] = EmailNormalizer.normalize(
                normalized["email"]
            )

        # Phone
        if "phone" in normalized:
            normalized["phone"] = PhoneNormalizer.normalize(
                normalized["phone"]
            )

        # Skills
        if "skills" in normalized:
            normalized["skills"] = SkillNormalizer.normalize(
                normalized["skills"]
            )

        return normalized