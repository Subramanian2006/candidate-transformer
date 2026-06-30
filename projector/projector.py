import json


class Projector:
    """
    Projects a canonical candidate into any requested
    output schema using a runtime configuration.
    """

    @staticmethod
    def load_config(config_path):

        with open(config_path, "r") as file:
            return json.load(file)

    @staticmethod
    def get_value(candidate, path):
        """
        Supports

        full_name

        emails[0]

        phones[0]
        """

        if "[" in path:

            field = path.split("[")[0]

            index = int(
                path.split("[")[1].replace("]", "")
            )

            values = candidate.get(field)

            if values is None:
                return None

            if index >= len(values):
                return None

            return values[index]

        return candidate.get(path)

    @classmethod
    def project(cls, candidate, config_path):

        config = cls.load_config(config_path)

        output = {}

        for field in config["fields"]:

            output_field = field["path"]

            source_field = field.get(
                "from",
                output_field,
            )

            value = cls.get_value(
                candidate,
                source_field,
            )

            output[output_field] = value

        if config.get("include_confidence", False):

            output["confidence"] = candidate.get(
                "confidence"
            )

        if config.get("include_provenance", False):

            output["provenance"] = candidate.get(
                "provenance"
            )

        return output