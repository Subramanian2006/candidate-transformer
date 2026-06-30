from extractor.csv_reader import CSVReader
from extractor.resume_reader import ResumeReader
from extractor.resume_parser import ResumeParser

from normalizer.candidate_normalizer import CandidateNormalizer

from matcher.candidate_matcher import CandidateMatcher

from merger.candidate_merger import CandidateMerger

from projector.projector import Projector
from validator.schema_validator import SchemaValidator


# ---------------- CSV ---------------- #

csv_candidate = CSVReader(
    "input/recruiter.csv"
).read()[0]

csv_candidate = CandidateNormalizer.normalize(
    csv_candidate
)

csv_candidate["source"] = "csv"

print("\n===== Normalized CSV =====")

print(csv_candidate)


# ---------------- Resume ---------------- #

resume_text = ResumeReader(
    "input/resume.pdf"
).read()

resume_candidate = ResumeParser(
    resume_text
).parse()

resume_candidate = CandidateNormalizer.normalize(
    resume_candidate
)

resume_candidate["source"] = "resume"

print("\n===== Normalized Resume =====")

print(resume_candidate)


# ---------------- Matcher ---------------- #

print("\n===== Candidate Matching =====")

matched, reason = CandidateMatcher.match(
    csv_candidate,
    resume_candidate,
)

print("Matched :", matched)
print("Reason  :", reason)


# ---------------- Merger ---------------- #

if matched:

    merged_candidate = CandidateMerger.merge(
        csv_candidate,
        resume_candidate,
    )

    print("\n===== Canonical Candidate =====")

    from pprint import pprint

    pprint(merged_candidate)

else:

    print("\nCandidates do not match.")

print("\n===== Default Output =====")

default_output = Projector.project(
    merged_candidate,
    "config/default.json",
)

default_output = SchemaValidator.validate(
    default_output,
    "config/default.json",
)

from pprint import pprint

pprint(default_output)


print("\n===== Custom Output =====")

custom_output = Projector.project(
    merged_candidate,
    "config/custom.json",
)

custom_output = SchemaValidator.validate(
    custom_output,
    "config/custom.json",
)

pprint(custom_output)