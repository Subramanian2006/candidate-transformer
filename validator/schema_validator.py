import json


class SchemaValidator:
    """
    Validates a projected candidate output
    against the projection configuration.
    """

    @staticmethod
    def load_config(config_path):
        with open(config_path, "r") as file:
            return json.load(file)

    @staticmethod
    def validate_type(value, expected_type):
        """
        Returns True if value matches expected type.
        """

        if value is None:
            return True

        if expected_type == "string":
            return isinstance(value, str)

        if expected_type == "number":
            return isinstance(value, (int, float))

        if expected_type == "boolean":
            return isinstance(value, bool)

        if expected_type == "string[]":

            if not isinstance(value, list):
                return False

            return all(
                isinstance(item, str)
                for item in value
            )

        return True

    @classmethod
    def validate(cls, projected_output, config_path):

        config = cls.load_config(config_path)

        validated = projected_output.copy()

        on_missing = config.get(
            "on_missing",
            "null"
        )

        for field in config["fields"]:

            field_name = field["path"]

            required = field.get(
                "required",
                False
            )

            expected_type = field.get(
                "type"
            )

            value = validated.get(field_name)

            # ---------------------------
            # Missing field validation
            # ---------------------------

            if required and value is None:

                if on_missing == "null":
                    validated[field_name] = None
                    continue

                if on_missing == "omit":
                    validated.pop(field_name, None)
                    continue

                if on_missing == "error":
                    raise ValueError(
                        f"Required field '{field_name}' is missing."
                    )

            # ---------------------------
            # Type validation
            # ---------------------------

            if value is not None:

                if not cls.validate_type(
                    value,
                    expected_type,
                ):

                    raise TypeError(
                        f"Field '{field_name}' "
                        f"expected '{expected_type}' "
                        f"but got '{type(value).__name__}'."
                    )

        return validated