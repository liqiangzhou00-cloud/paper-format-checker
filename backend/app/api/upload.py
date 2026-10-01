from __future__ import annotations

from typing import Any, Dict, List

from app.models.document_model import DocumentModel
from app.services.detailed_checker import DetailedChecker
from app.services.docx_parser import DocxParser


class CheckPipeline:
    def __init__(self):
        self.parser = DocxParser()
        self.checker = DetailedChecker()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        document: DocumentModel
        if "file_bytes" in payload:
            document = self.parser.extract_from_docx_bytes(payload["file_bytes"])
        else:
            document = self.parser.parse(payload)

        issues: List[Dict[str, Any]] = []
        issues.extend(self.checker.check_cover(document))
        issues.extend(self.checker.check_abstract(document))
        issues.extend(self.checker.check_sections(document))
        issues.extend(self.checker.check_references(document))
        issues.extend(self.checker.check_figures_tables(document))
        issues.extend(self.checker.check_styles(document))
        issues.extend(self.checker.check_pagination(document))

        summary = {
            "error": sum(1 for item in issues if item.get("severity") == "error"),
            "warning": sum(1 for item in issues if item.get("severity") == "warning"),
            "info": sum(1 for item in issues if item.get("severity") == "info"),
        }

        return {
            "summary": summary,
            "issues": issues,
            "document_info": {
                "title": document.title,
                "english_title": document.english_title,
                "sections_count": len(document.sections),
                "figures_count": len(document.figures),
                "tables_count": len(document.tables),
                "references_count": len(document.references),
            },
        }
