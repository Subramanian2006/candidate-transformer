from dateutil import parser


class DateNormalizer:

    @staticmethod
    def normalize(date_string):

        if not date_string:
            return None

        try:

            dt = parser.parse(date_string)

            return dt.strftime("%Y-%m")

        except Exception:

            return None