import hashlib


class CandidateMerger:
    """
    Merges normalized candidate records into a single
    canonical profile with provenance and confidence.
    """

    # Map singular input keys to canonical plural keys
    KEY_MAPPING = {
        "email": "emails",
        "phone": "phones"
    }

    @staticmethod
    def generate_candidate_id(candidate):
        """
        Generate a deterministic candidate id.
        """
        base = (
            candidate.get("full_name", "")
            + candidate.get("email", "")
        )

        return hashlib.sha256(base.encode()).hexdigest()[:12]

    @staticmethod
    def merge_scalar(csv_value, resume_value):
        """
        Structured source (CSV) has higher priority.
        """
        return csv_value if csv_value is not None else resume_value

    @staticmethod
    def merge_list(*lists):
        """
        Merge lists while removing duplicates.
        """
        merged = []

        for lst in lists:

            if lst is None:
                continue

            if not isinstance(lst, list):
                lst = [lst]

            for item in lst:
                if item and item not in merged:
                    merged.append(item)

        return merged

    @staticmethod
    def calculate_field_confidence(csv_value, resume_value):
        """
        Dynamic confidence calculation.

        Rules

        Both agree        -> 0.95
        Both conflict     -> 0.70
        Only CSV          -> 0.90
        Only Resume       -> 0.80
        Missing           -> 0.00
        """

        if csv_value is not None and resume_value is not None:

            if csv_value == resume_value:
                return 0.95

            return 0.70

        if csv_value is not None:
            return 0.90

        if resume_value is not None:
            return 0.80

        return 0.0

    @classmethod
    def build_confidence(cls, csv_candidate, resume_candidate):

        confidence = {}

        fields = set(csv_candidate.keys()) | set(resume_candidate.keys())

        ignored = {"source"}

        for field in fields:

            if field in ignored:
                continue
            
            # Use the canonical name if it exists in the mapping, else use the original
            canonical_field = cls.KEY_MAPPING.get(field, field)

            confidence[canonical_field] = cls.calculate_field_confidence(
                csv_candidate.get(field),
                resume_candidate.get(field),
            )

        return confidence

    @staticmethod
    def build_provenance(csv_candidate, resume_candidate):

        provenance = {}

        fields = set(csv_candidate.keys()) | set(resume_candidate.keys())

        ignored = {"source"}

        for field in fields:

            if field in ignored:
                continue
                
            # Use the canonical name if it exists in the mapping, else use the original
            canonical_field = CandidateMerger.KEY_MAPPING.get(field, field)

            csv_exists = csv_candidate.get(field) is not None
            resume_exists = resume_candidate.get(field) is not None

            if csv_exists and resume_exists:

                provenance[canonical_field] = [
                    csv_candidate["source"],
                    resume_candidate["source"],
                ]

            elif csv_exists:

                provenance[canonical_field] = csv_candidate["source"]

            elif resume_exists:

                provenance[canonical_field] = resume_candidate["source"]

        return provenance

    @classmethod
    def merge(cls, csv_candidate, resume_candidate):

        merged = {}

        merged["candidate_id"] = cls.generate_candidate_id(
            csv_candidate
        )

        merged["full_name"] = cls.merge_scalar(
            csv_candidate.get("full_name"),
            resume_candidate.get("full_name"),
        )

        merged["emails"] = cls.merge_list(
            csv_candidate.get("email"),
            resume_candidate.get("email"),
        )

        merged["phones"] = cls.merge_list(
            csv_candidate.get("phone"),
            resume_candidate.get("phone"),
        )

        merged["current_company"] = cls.merge_scalar(
            csv_candidate.get("current_company"),
            resume_candidate.get("current_company"),
        )

        merged["title"] = cls.merge_scalar(
            csv_candidate.get("title"),
            resume_candidate.get("title"),
        )

        merged["skills"] = cls.merge_list(
            csv_candidate.get("skills"),
            resume_candidate.get("skills"),
        )

        merged["provenance"] = cls.build_provenance(
            csv_candidate,
            resume_candidate,
        )

        merged["confidence"] = cls.build_confidence(
            csv_candidate,
            resume_candidate,
        )

        scores = [
            score
            for score in merged["confidence"].values()
            if score > 0
        ]

        merged["overall_confidence"] = round(
            sum(scores) / len(scores),
            2,
        )

        return merged