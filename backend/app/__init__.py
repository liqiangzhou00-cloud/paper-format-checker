from __future__ import annotations

from typing import Any, Dict, List

from app.models import CheckReport, CheckResponse


class ReportService:
    def build_response(self, report: CheckReport) -> CheckResponse:
        issues = [
            {
                "rule_id": issue.rule_id,
                "title": issue.title,
                "severity": issue.severity,
                "description": issue.description,
                "location": issue.location,
                "suggestion": issue.suggestion,
            }
            for issue in report.issues
        ]
        return CheckResponse(summary=report.summary, issues=issues)
