from __future__ import annotations

from typing import Any, Dict, List, Sequence

from app.config.rules import load_rules
from app.models import CheckReport, Issue


class DocumentParser:
    def parse(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if hasattr(payload, "__dict__"):
            payload = payload.__dict__

        sections = payload.get("sections", []) or []
        references = payload.get("references", []) or []
        figures = payload.get("figures", []) or []
        tables = payload.get("tables", []) or []

        return {
            "title": str(payload.get("title", "")).strip(),
            "english_title": str(payload.get("english_title", "")).strip(),
            "abstract": str(payload.get("abstract", "")).strip(),
            "keywords": payload.get("keywords", []) or [],
            "sections": sections,
            "references": references,
            "figures": figures,
            "tables": tables,
        }


class RuleEngine:
    def __init__(self):
        self.rules = load_rules()
        self.parser = DocumentParser()

    def evaluate(self, payload: Any) -> CheckReport:
        doc = self.parser.parse(payload)
        report = CheckReport()

        if not doc["title"]:
            report.issues.append(self._issue("COVER_TITLE_ALIGNMENT", "Title is missing", "error", "The paper title is required.", "cover", "Add the title on the cover page."))

        if doc["abstract"] and len(doc["abstract"]) < 500:
            report.issues.append(self._issue("ABSTRACT_LENGTH", "Abstract is too short", "warning", "The abstract should be at least 500 Chinese characters long.", "abstract", "Expand the abstract to include the purpose, methods, results, and conclusion."))

        if not doc["sections"]:
            report.issues.append(self._issue("SECTION_LEVELING", "No section structure found", "warning", "The paper should contain chapter and section structure.", "section", "Add chapter headings and subordinate sections."))

        for section in doc["sections"]:
            title = str(section.get("title", "")).strip()
            level = int(section.get("level", 1) or 1)
            if level not in {1, 2, 3}:
                report.issues.append(self._issue("SECTION_LEVELING", "Invalid section level", "warning", f"Section '{title}' uses level {level}.", "section", "Adjust the section hierarchy to 1, 2, or 3."))
            if "本章小结" in title and section.get("level") == 1:
                report.issues.append(self._issue("CHAPTER_SUMMARY", "Summary in the first chapter", "info", "The summary should appear from chapter 2 onward.", "section", "Move or remove the summary section from the first chapter."))

        if len(doc["references"]) < 15:
            report.issues.append(self._issue("REFERENCE_MIN_COUNT", "Reference count is low", "warning", "The paper should include at least 15 references.", "references", "Expand the reference list to meet the minimum requirement."))

        refs = doc["references"]
        ids = [int(ref.get("id", 0) or 0) for ref in refs if isinstance(ref, dict)]
        if ids and ids != list(range(1, max(ids) + 1)):
            report.issues.append(self._issue("REFERENCE_SEQUENCE", "Reference numbers are not sequential", "error", "Reference numbers should begin at 1 and increase without gaps.", "references", "Renumber the reference list in order."))

        for figure in doc["figures"]:
            caption = str(figure.get("caption", "")).strip()
            if caption and not caption.startswith("图"):
                report.issues.append(self._issue("FIGURE_CAPTION_FORMAT", "Incorrect figure caption", "error", "Figure captions should start with '图' and use the correct numbering format.", "figure", "Add a caption like '图2-1'."))

        for table in doc["tables"]:
            caption = str(table.get("caption", "")).strip()
            if caption and not caption.startswith("表"):
                report.issues.append(self._issue("TABLE_CAPTION_FORMAT", "Incorrect table caption", "error", "Table captions should start with '表' and use the correct numbering format.", "table", "Add a caption like '表3-1'."))

        report.summary = {
            "error": sum(1 for issue in report.issues if issue.severity == "error"),
            "warning": sum(1 for issue in report.issues if issue.severity == "warning"),
            "info": sum(1 for issue in report.issues if issue.severity == "info"),
        }
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
