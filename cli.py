import argparse
import json

from extractor.csv_reader import CSVReader
from extractor.resume_reader import ResumeReader
from extractor.resume_parser import ResumeParser

from normalizer.candidate_normalizer import CandidateNormalizer
from matcher.candidate_matcher import CandidateMatcher
from merger.candidate_merger import CandidateMerger

from projector.projector import Projector
from validator.schema_validator import SchemaValidator


def main():

    parser = argparse.ArgumentParser(
        description="Candidate Transformer CLI"
    )

    parser.add_argument(
        "--csv",
        required=True,
        help="Path to recruiter CSV"
    )

    parser.add_argument(
        "--resume",
        required=True,
        help="Path to resume PDF"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Projection config JSON"
    )

    parser.add_argument(
        "--output",
        default="output/result.json",
        help="Output JSON file"
    )

    args = parser.parse_args()

    # ---------- CSV ----------

    csv_candidate = CSVReader(args.csv).read()[0]

    csv_candidate = CandidateNormalizer.normalize(
        csv_candidate
    )

    csv_candidate["source"] = "csv"

    # ---------- Resume ----------

    resume_text = ResumeReader(
        args.resume
    ).read()

    resume_candidate = ResumeParser(
        resume_text
    ).parse()

    resume_candidate = CandidateNormalizer.normalize(
        resume_candidate
    )

    resume_candidate["source"] = "resume"

    # ---------- Matching ----------

    matched, reason = CandidateMatcher.match(
        csv_candidate,
        resume_candidate
    )

    if not matched:
        print("Candidates do not match.")
        print("Reason:", reason)
        return

    # ---------- Merge ----------

    merged_candidate = CandidateMerger.merge(
        csv_candidate,
        resume_candidate
    )

    # ---------- Projection ----------

    output = Projector.project(
        merged_candidate,
        args.config
    )

    output = SchemaValidator.validate(
        output,
        args.config
    )

    # ---------- Save ----------

    with open(
        args.output,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=4
        )

    print("\nTransformation Successful!")

    print("Output saved to")

    print(args.output)


if __name__ == "__main__":
    main()