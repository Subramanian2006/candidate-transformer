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
#python cli.py --csv input/recruiter.csv --resume input/resume.pdf --config config/custom.json

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

    csv_records = CSVReader(args.csv).read()

    if csv_records:
        csv_candidate = CandidateNormalizer.normalize(csv_records[0])
        csv_candidate["source"] = "csv"
    else:
        print("[Warning] CSV could not be loaded.")
        csv_candidate = {}
    # ---------- Resume ----------

    resume_text = ResumeReader(args.resume).read()

    if resume_text:
        resume_candidate = ResumeParser(resume_text).parse()
        resume_candidate = CandidateNormalizer.normalize(resume_candidate)
        resume_candidate["source"] = "resume"
    else:
        print("[Warning] Resume could not be loaded.")
        resume_candidate = {}

    # ---------- Matching ----------

    # Case 1: Neither source available
    if not csv_candidate and not resume_candidate:
        print("No valid candidate sources found.")
        return

    # Case 2: Only CSV available
    elif csv_candidate and not resume_candidate:
        print("\nOnly CSV source available. Building profile from CSV.")
        merged_candidate = CandidateMerger.merge(
            csv_candidate,
            {}
        )

    # Case 3: Only Resume available
    elif resume_candidate and not csv_candidate:
        print("\nOnly Resume source available. Building profile from Resume.")
        merged_candidate = CandidateMerger.merge(
            {},
            resume_candidate
        )

    # Case 4: Both sources available
    else:

        print("\n===== Candidate Matching =====")

        matched, reason = CandidateMatcher.match(
            csv_candidate,
            resume_candidate
        )

        print("Matched :", matched)
        print("Reason  :", reason)

        if not matched:
            print("Candidates do not match.")
            return

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
