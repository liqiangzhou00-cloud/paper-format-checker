from __future__ import annotations

from typing import Any, Dict, List

from app.checkers import CoverChecker, FigureTableChecker, LayoutChecker, ReferenceChecker, SectionChecker, StyleChecker
from app.config.rules import load_rules
from app.models import CheckReport, Issue


class DocumentParser:
    def parse(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if hasattr(payload, "__dict__"):
            payload = payload.__dict__

        return {
            "title": str(payload.get("title", "")).strip(),
            "english_title": str(payload.get("english_title", "")).strip(),
            "abstract": str(payload.get("abstract", "")).strip(),
            "keywords": payload.get("keywords", []) or [],
            "sections": payload.get("sections", []) or [],
            "references": payload.get("references", []) or [],
            "figures": payload.get("figures", []) or [],
            "tables": payload.get("tables", []) or [],
            "paragraphs": payload.get("paragraphs", []) or [],
            "pages": payload.get("pages", {}) or {},
        }


class RuleEngine:
    def __init__(self):
        self.rules = load_rules()
        self.parser = DocumentParser()
        self.cover_checker = CoverChecker()
        self.section_checker = SectionChecker()
        self.reference_checker = ReferenceChecker()
        self.figure_table_checker = FigureTableChecker()
        self.style_checker = StyleChecker()
        self.layout_checker = LayoutChecker()

    def evaluate(self, payload: Any) -> CheckReport:
        doc = self.parser.parse(payload)
        report = CheckReport()

        report.issues.extend(self._transform_issues(self.cover_checker.check(doc["title"], doc["english_title"], doc["keywords"], doc["abstract"])))
        report.issues.extend(self._transform_issues(self.section_checker.check(doc["sections"])))
        report.issues.extend(self._transform_issues(self.reference_checker.check(doc["references"])))
        report.issues.extend(self._transform_issues(self.figure_table_checker.check(doc["figures"], doc["tables"])))
        report.issues.extend(self._transform_issues(self.style_checker.check(doc["paragraphs"])))
        report.issues.extend(self._transform_issues(self.layout_checker.check(doc["pages"])))

        report.summary = {
            "error": sum(1 for issue in report.issues if issue.severity == "error"),
            "warning": sum(1 for issue in report.issues if issue.severity == "warning"),
            "info": sum(1 for issue in report.issues if issue.severity == "info"),
        }
        return report

    def _transform_issues(self, raw_issues: List[Dict[str, str]]) -> List[Issue]:
        transformed = []
        for item in raw_issues:
            transformed.append(
                Issue(
                    rule_id=item.get("rule_id", "UNKNOWN_RULE"),
                    title=item.get("rule_id", "UNKNOWN_RULE"),
                    severity=item.get("severity", "info"),
                    description=item.get("message", "No description available."),
                    location=item.get("location", "general"),
                    suggestion=item.get("suggestion", "Review the template requirement."),
                )
            )
        return transformed
