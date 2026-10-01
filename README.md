# paper-format-checker

A web-based paper format checker system for validating academic paper formatting standards.

## Overview
This project provides a rule-driven workflow to check academic paper formatting against graduation thesis requirements, including:
- cover page layout
- title formatting
- abstract and keywords
- chapter structure and page numbering
- tables, figures, and formulas
- references and citation numbering
- appendix and acknowledgments

## Architecture
- Backend: Python + FastAPI
- Frontend: static HTML + JavaScript
- Rules: YAML config for format validation
- Reporting: structured issue list with severity and suggestions

## Quick start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
Open `frontend/index.html` in a browser, or serve it with a local static server.

### Example API request
```bash
curl -X POST http://localhost:8000/api/check \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Smart Campus WLAN Networking Design",
    "abstract": "This paper analyzes the design of a campus wireless network.",
    "keywords": ["WLAN", "network design", "campus security"],
    "sections": [
      {"title": "绪论", "level": 1},
      {"title": "本章小结", "level": 2},
      {"title": "总结与展望", "level": 1}
    ],
    "references": [
      {"id": 1, "text": "IEEE 802.11 standard"},
      {"id": 2, "text": "WLAN security article"}
    ]
  }'
```

## Core modules
- Document parser
- Section and structure checker
- Style validator
- Figure/table validator
- Reference checker
- Result reporter

## Notes
This repository is an MVP implementation for the core modules required for a web-based academic paper format checker.
