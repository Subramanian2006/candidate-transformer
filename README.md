# Multi-Source Candidate Data Transformer

A modular candidate data transformation pipeline built for the **Eightfold Engineering Intern (Jul–Dec 2026) Assignment**.

The system ingests candidate information from multiple heterogeneous sources, transforms it into a single canonical profile, tracks provenance and confidence for every field, and produces configurable outputs using a runtime JSON configuration.

---

## Features

- Read candidate information from:
  - Structured Source: Recruiter CSV
  - Unstructured Source: Resume PDF
- Extract candidate information
- Normalize names, emails, phone numbers, and skills
- Deterministic candidate matching
- Merge multiple records into a canonical profile
- Dynamic confidence calculation
- Provenance tracking
- Runtime configurable output projection
- Schema validation
- Command Line Interface (CLI)
- Unit tests

---

## Project Architecture

```
Recruiter CSV
                \
                 \
                  --> Extraction
                 /
Resume PDF -----/

        ↓

Normalization

        ↓

Candidate Matching

        ↓

Candidate Merger

        ↓

Canonical Candidate

        ↓

Projection Engine

        ↓

Schema Validator

        ↓

Final JSON Output
```

---

## Project Structure

```
candidate-transformer/

├── cli.py
├── main.py
│
├── config/
│   ├── default.json
│   └── custom.json
│
├── extractor/
│
├── matcher/
│
├── merger/
│
├── normalizer/
│
├── projector/
│
├── validator/
│
├── input/
│
├── output/
│
├── tests/
│
└── README.md
```

---

## Requirements

- Python 3.10+
- pandas
- pymupdf
- phonenumbers
- python-dateutil
- rapidfuzz
- jsonschema

Install dependencies:

```bash
pip install pandas pymupdf phonenumbers python-dateutil rapidfuzz jsonschema
```

---

## Running the CLI

Default configuration:

```bash
python cli.py --csv input/recruiter.csv --resume input/resume.pdf --config config/default.json
```

Custom configuration:

```bash
python cli.py --csv input/recruiter.csv --resume input/resume.pdf --config config/custom.json
```

The transformed output is saved to:

```
output/result.json
```

---

## Demo Mode

For demonstration and debugging, run:

```bash
python main.py
```

This prints every stage of the pipeline including:

- Normalized CSV
- Normalized Resume
- Candidate Matching
- Canonical Candidate
- Default Projection
- Custom Projection

---

## Sample Canonical Output

```json
{
    "candidate_id": "b4353ed163af",
    "full_name": "kr subramanian",
    "emails": [
        "krsubbu@gmail.com",
        "krsubramanian2006@gmail.com"
    ],
    "phones": [
        "+919876543210",
        "+917358459535"
    ],
    "skills": [
        "Python",
        "Flask",
        "MySQL"
    ]
}
```

---

## Runtime Configuration

The output schema is completely configurable.

Supported features:

- Select fields
- Rename fields
- Field mapping
- Array indexing (`emails[0]`)
- Enable/disable provenance
- Enable/disable confidence
- Missing value policies
- Schema validation

Example:

```json
{
    "fields": [
        {
            "path": "candidate_name",
            "from": "full_name"
        },
        {
            "path": "primary_email",
            "from": "emails[0]"
        }
    ]
}
```

---

## Testing

Run the tests:

```bash
python tests/test_normalizer.py

python tests/test_matcher.py

python tests/test_validator.py
```

---

## Design Decisions

- Separate internal canonical representation from output projection.
- Use deterministic candidate matching instead of probabilistic matching.
- Structured data is given higher priority during merging.
- Unknown values are never invented; missing values are handled according to the configured policy.
- Confidence scores are computed dynamically based on agreement between sources.

---

## Edge Cases Handled

- Missing resume fields
- Missing CSV values
- Invalid phone numbers
- Multiple emails
- Duplicate skills
- Malformed configuration
- Required field validation
- Type validation
- Candidate mismatch

---

## Future Improvements

- LinkedIn integration
- GitHub API integration
- ATS JSON support
- OCR for scanned resumes
- Fuzzy company matching
- LLM-assisted resume parsing
- REST API deployment

---

## Assignment Deliverables

- One-page design document
- Runnable GitHub repository
- Runtime configurable pipeline
- Sample outputs
- Unit tests
- Demo video
