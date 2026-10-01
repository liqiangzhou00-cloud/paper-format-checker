# paper-format-checker

A web-based paper format checker for validating academic thesis formatting against the graduation thesis template.

## Overview
This project provides a rule-driven workflow for checking academic paper formatting, including:
- cover page and metadata
- abstract and keywords
- chapter structure and summary sections
- figure and table numbering
- reference numbering and bibliography rules
- appendix and acknowledgement checks
- document sizing and editorial consistency

## Architecture
- Backend: Python + FastAPI
- Frontend: HTML + JavaScript
- Rule engine: modular checkers
- Data model: structured document model
- Report: JSON/HTML summary output

## Repository structure
```text
paper-format-checker/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── upload.py
│   │   ├── checkers/
│   │   │   ├── __init__.py
│   │   │   ├── cover_checker.py
│   │   │   ├── figure_table_checker.py
│   │   │   ├── layout_checker.py
│   │   │   ├── reference_checker.py
│   │   │   ├── section_checker.py
│   │   │   └── style_checker.py
│   │   ├── config/
│   │   │   ├── rules.py
│   │   │   └── rules.yaml
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── document_model.py
│   │   ├── services/
│   │   │   ├── check_pipeline.py
│   │   │   ├── docx_parser.py
│   │   │   ├── report_export.py
│   │   │   └── rule_engine.py
│   │   ├── __init__.py
│   │   └── main.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── upload.html
│   ├── upload.js
│   ├── report.html
│   ├── report.js
│   └── styles.css
├── docs/
│   └── paper-format-rules.md
├── .gitignore
└── README.md
```

## Quick start

### 1. Install backend dependencies
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run backend service
```bash
cd backend
python run.py
```
The service will start on:
- http://localhost:8000

### 3. Open the frontend
Open the HTML page directly in a browser:
- frontend/upload.html

Or use a simple static server if needed:
```bash
cd frontend
python -m http.server 8080
```
Then open:
- http://localhost:8080/upload.html

## API
### Upload file
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@sample.docx"
```

Returns a JSON payload with a summary and issue list.

## Example response
```json
{
  "summary": {
    "error": 2,
    "warning": 4,
    "info": 1
  },
  "issues": [
    {
      "rule_id": "COVER_TITLE_ALIGNMENT",
      "severity": "error",
      "message": "The paper title is missing.",
      "location": "cover",
      "suggestion": "Add the title on the cover page."
    }
  ]
}
```

## Development notes
This project is an MVP rule-based format checker designed for thesis-template validation. It is structured for future extension to:
- automatic DOCX parsing
- template configuration by academic college
- improved issue detail mapping to Word locations
- PDF/HTML report export

## Next steps
- integrate full DOCX parsing engine
- improve issue mapping to specific sections
- support multiple thesis templates
- add export to PDF/HTML report
