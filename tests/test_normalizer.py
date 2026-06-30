import os
import sys

# Allow imports from the project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from pprint import pprint

from normalizer.candidate_normalizer import CandidateNormalizer


def test_candidate_normalizer():

    raw_candidate = {
        "full_name": "KR. SUBRAMANIAN",
        "email": "KRSubbu@GMAIL.com",
        "phone": "9876543210",
        "skills": [
            "python",
            "HTML",
            "mysql",
            "vue.js"
        ]
    }

    expected = {
        "full_name": "kr subramanian",
        "email": "krsubbu@gmail.com",
        "phone": "+919876543210",
        "skills": [
            "HTML",
            "MySQL",
            "Python",
            "Vue"
        ]
    }

    normalized = CandidateNormalizer.normalize(raw_candidate)

    print("\n========== Candidate Normalizer Test ==========")

    print("\nInput Candidate:")
    pprint(raw_candidate)

    print("\nNormalized Candidate:")
    pprint(normalized)

    print("\nExpected Candidate:")
    pprint(expected)

    print("\nRunning Assertions...")

    assert normalized["full_name"] == expected["full_name"], \
        "❌ Full Name normalization failed."

    assert normalized["email"] == expected["email"], \
        "❌ Email normalization failed."

    assert normalized["phone"] == expected["phone"], \
        "❌ Phone normalization failed."

    assert normalized["skills"] == expected["skills"], \
        "❌ Skill normalization failed."

    print("\n✅ All normalization tests passed successfully!")


if __name__ == "__main__":
    test_candidate_normalizer()