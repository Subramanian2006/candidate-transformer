import phonenumbers


class PhoneNormalizer:

    @staticmethod
    def normalize(phone, default_region="IN"):
        """
        Convert phone numbers into E.164 format.
        Returns None if the number is invalid.
        """

        if phone is None:
            return None

        try:
            phone = str(phone).strip()

            parsed = phonenumbers.parse(phone, default_region)

            if not phonenumbers.is_valid_number(parsed):
                return None

            return phonenumbers.format_number(
                parsed,
                phonenumbers.PhoneNumberFormat.E164
            )

        except Exception:
            return None