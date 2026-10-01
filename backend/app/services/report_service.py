from __future__ import annotations

import re
from typing import Any, Dict, List

from app.models import CheckReport, Issue
from app.config.rules import load_rules


class DocumentParser:
    def parse(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sections = payload.get("sections", [])
        references = payload.get("references", [])
        figures = payload.get("figures", [])
        tables = payload.get("tables", [])

        normalized = {
            "title": payload.get("title", ""),
            "english_title": payload.get("english_title", ""),
            "abstract": payload.get("abstract", ""),
            "keywords": payload.get("keywords", []),
            "sections": sections,
            "references": references,
            "figures": figures,
            "tables": tables,
            "citation_markers": self._extract_citation_markers(payload),
        }
        return normalized

    def _extract_citation_markers(self, payload: Dict[str, Any]) -> List[int]:
        text = "\n".join(str(item.get("text", "")) for item in payload.get("references", []))
        matches = re.findall(r"\[(\d+)\]", text)
        return [int(m) for m in matches]


class RuleEngine:
    def __init__(self):
        self.rules = load_rules()
        self.parser = DocumentParser()

    def evaluate(self, payload: Any) -> CheckReport:
        doc = self.parser.parse(payload.__dict__ if hasattr(payload, "__dict__") else payload)
        report = CheckReport()

        if not doc["title"]:
            report.issues.append(self._issue("COVER_TITLE_ALIGNMENT", "Title is missing", "error", "The cover title is required.", "cover", "Add a proper title to the cover page."))

        if doc["abstract"] and len(doc["abstract"]) < 500:
            report.issues.append(self._issue("ABSTRACT_LENGTH", "Abstract too short", "warning", "Abstract length is below the recommended minimum.", "abstract", "Expand the abstract to match the style requirement."))

        if len(doc["sections"]) < 2:
            report.issues.append(self._issue("SECTION_LEVELING", "Insufficient section structure", "warning", "The document should include the main chapter structure.", "section", "Add a proper chapter structure."))

        if len(doc["references"]) < 15:
            report.issues.append(self._issue("REFERENCE_MIN_COUNT", "Reference list is too short", "warning", "The document should contain enough references.", "references", "Add more references to meet the minimum requirement."))

        if doc["sections"]:
            for idx, section in enumerate(doc["sections"], start=1):
                title = str(section.get("title", ""))
                level = int(section.get("level", 1) or 1)
                if level not in {1, 2, 3}:
                    report.issues.append(self._issue("SECTION_LEVELING", f"Section level issue at {idx}", "warning", f"The heading level {level} is outside the expected range.", f"section:{idx}", "Adjust the section hierarchy."))
                if "本章小结" in title and idx == 1:
                    report.issues.append(self._issue("CHAPTER_SUMMARY", "Summary not allowed in the first chapter", "info", "Only chapters after the first should use a summary section.", "section:1", "Remove or relocate the summary section."))

        if doc["figures"]:
            for item in doc["figures"]:
                caption = str(item.get("caption", ""))
                if not caption.startswith("图"):
                    report.issues.append(self._issue("FIGURE_CAPTION_FORMAT", "Figure caption format issue", "error", "Figure numbering should use a '图X-X' format.", "figure", "Set the caption to a valid figure format."))

        if doc["tables"]:
            for item in doc["tables"]:
                caption = str(item.get("caption", ""))
                if not caption.startswith("表"):
                    report.issues.append(self._issue("TABLE_CAPTION_FORMAT", "Table caption format issue", "error", "Table numbering should use a '表X-X' format.", "table", "Set the caption to a valid table format."))

        if doc["references"]:
            ids = [int(item.get("id", 0)) for item in doc["references"]]
            if ids and ids != list(range(1, max(ids) + 1)):
                report.issues.append(self._issue("REFERENCE_SEQUENCE", "Reference numbers are not sequential", "error", "References should begin at 1 and be numbered sequentially.", "references", "Renumber the references in the correct order."))

        report.summary = {"error": sum(1 for i in report.issues if i.severity == "error"), "warning": sum(1 for i in report.issues if i.severity == "warning"), "info": sum(1 for i in report.issues if i.severity == "info")}
        return report

    def _issue(self, rule_id: str, title: str, severity: str, description: str, location: str, suggestion: str) -> Issue:
        return Issue(
            rule_id=rule_id,
            title=title,
            severity=severity,
            description=description,
            location=location,
            suggestion=suggestion,
        )
