import pandas as pd


class CSVReader:
    """
    Reads recruiter CSV files and returns
    a list of candidate dictionaries.
    """

    REQUIRED_COLUMNS = [
        "full_name",
        "email",
        "phone",
        "current_company",
        "title",
    ]

    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        try:
            df = pd.read_csv(self.file_path)

            missing = [
                col for col in self.REQUIRED_COLUMNS
                if col not in df.columns
            ]

            if missing:
                raise ValueError(
                    f"Missing columns: {missing}"
                )

            return df.to_dict(orient="records")

        except Exception as e:
            print(f"[CSV Reader Error] {e}")
            return []