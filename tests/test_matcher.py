import os
import sys

# Allow imports from the project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from matcher.candidate_matcher import CandidateMatcher


def run_test(test_name, candidate1, candidate2, expected_match, expected_reason):

    print(f"\n========== {test_name} ==========")

    print("\nCandidate 1:")
    print(candidate1)

    print("\nCandidate 2:")
    print(candidate2)

    matched, reason = CandidateMatcher.match(
        candidate1,
        candidate2
    )

    print("\nActual Result")
    print("Matched :", matched)
    print("Reason  :", reason)

    print("\nExpected Result")
    print("Matched :", expected_match)
    print("Reason  :", expected_reason)

    assert matched == expected_match, \
        f"❌ Match result incorrect for {test_name}"

    assert reason == expected_reason, \
        f"❌ Match reason incorrect for {test_name}"

    print(f"\n✅ {test_name} Passed!")


def test_candidate_matcher():

    # -------------------------------------------------
    # Test 1 : Email Match
    # -------------------------------------------------

    candidate1 = {
        "email": "abc@gmail.com",
        "phone": "+919999999999",
        "full_name": "john doe"
    }

    candidate2 = {
        "email": "abc@gmail.com",
        "phone": "+918888888888",
        "full_name": "different person"
    }

    run_test(
        "Email Match Test",
        candidate1,
        candidate2,
        True,
        "Matched by Email"
    )

    # -------------------------------------------------
    # Test 2 : Phone Match
    # -------------------------------------------------

    candidate1 = {
        "email": "abc@gmail.com",
        "phone": "+919999999999",
        "full_name": "john doe"
    }

    candidate2 = {
        "email": "xyz@gmail.com",
        "phone": "+919999999999",
        "full_name": "another person"
    }

    run_test(
        "Phone Match Test",
        candidate1,
        candidate2,
        True,
        "Matched by Phone"
    )

    # -------------------------------------------------
    # Test 3 : Full Name Match
    # -------------------------------------------------

    candidate1 = {
        "email": "abc@gmail.com",
        "phone": "+911111111111",
        "full_name": "kr subramanian"
    }

    candidate2 = {
        "email": "xyz@gmail.com",
        "phone": "+922222222222",
        "full_name": "kr subramanian"
    }

    run_test(
        "Full Name Match Test",
        candidate1,
        candidate2,
        True,
        "Matched by Full Name"
    )

    # -------------------------------------------------
    # Test 4 : No Match
    # -------------------------------------------------

    candidate1 = {
        "email": "abc@gmail.com",
        "phone": "+911111111111",
        "full_name": "john doe"
    }

    candidate2 = {
        "email": "xyz@gmail.com",
        "phone": "+922222222222",
        "full_name": "jane smith"
    }

    run_test(
        "No Match Test",
        candidate1,
        candidate2,
        False,
        "No Match Found"
    )


if __name__ == "__main__":
    test_candidate_matcher()