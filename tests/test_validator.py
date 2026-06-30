import os
import sys
import json
import tempfile

# Allow imports from project root
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from validator.schema_validator import SchemaValidator


def create_temp_config(config_data):
    """
    Creates a temporary config JSON file.
    """

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".json",
        mode="w"
    )

    json.dump(config_data, temp, indent=4)

    temp.close()

    return temp.name


def test_validator():

    print("\n========== Validator Tests ==========")

    # --------------------------------------------------
    # Test 1 : Valid Output
    # --------------------------------------------------

    config = {
        "fields": [
            {
                "path": "candidate_name",
                "type": "string",
                "required": True
            },
            {
                "path": "skills",
                "type": "string[]"
            }
        ],
        "on_missing": "error"
    }

    output = {
        "candidate_name": "KR Subramanian",
        "skills": [
            "Python",
            "Flask"
        ]
    }

    config_file = create_temp_config(config)

    validated = SchemaValidator.validate(
        output,
        config_file
    )

    print("\n✅ Valid Output Test Passed")
    print(validated)

    # --------------------------------------------------
    # Test 2 : Missing Required Field
    # --------------------------------------------------

    config = {
        "fields": [
            {
                "path": "candidate_name",
                "type": "string",
                "required": True
            }
        ],
        "on_missing": "null"
    }

    output = {}

    config_file = create_temp_config(config)

    validated = SchemaValidator.validate(
        output,
        config_file
    )

    assert validated["candidate_name"] is None

    print("\n✅ Missing Field Test Passed")
    print(validated)

    # --------------------------------------------------
    # Test 3 : Wrong Type
    # --------------------------------------------------

    config = {
        "fields": [
            {
                "path": "skills",
                "type": "string[]"
            }
        ],
        "on_missing": "error"
    }

    output = {
        "skills": "Python"
    }

    config_file = create_temp_config(config)

    try:

        SchemaValidator.validate(
            output,
            config_file
        )

    except TypeError as e:

        print("\n✅ Type Validation Test Passed")
        print(e)

    else:

        raise AssertionError(
            "❌ Type validation failed."
        )


if __name__ == "__main__":
    test_validator()