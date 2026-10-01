from __future__ import annotations

from typing import Any, Dict, List

from app.models.document_model import DocumentModel
from app.services.docx_parser import DocxParser
from app.checkers import CoverChecker, FigureTableChecker, LayoutChecker, ReferenceChecker, SectionChecker, StyleChecker


class CheckPipeline:
    def __init__(self):
        self.parser = DocxParser()
        self.cover_checker = CoverChecker()
        self.section_checker = SectionChecker()
        self.reference_checker = ReferenceChecker()
        self.figure_table_checker = FigureTableChecker()
        self.style_checker = StyleChecker()
        self.layout_checker = LayoutChecker()

    def run(self, payload: Dict[str, Any]) -> List[Dict[str, str]]:
        document = self.parser.parse(payload)
        issues = []

        issues.extend(self.cover_checker.check(document.title, document.english_title, document.keywords, document.abstract))
        issues.extend(self.section_checker.check([{"title": s.title, "level": s.level} for s in document.sections]))
        issues.extend(self.reference_checker.check([{"id": ref.id, "text": ref.text} for ref in document.references]))
        issues.extend(self.figure_table_checker.check(
            [{"caption": fig.caption} for fig in document.figures],
            [{"caption": table.caption} for table in document.tables],
        ))
        issues.extend(self.style_checker.check([
            {"font": p.font, "align": p.align} for p in document.paragraphs
        ]))
        issues.extend(self.layout_checker.check(document.pages))

        return issues
