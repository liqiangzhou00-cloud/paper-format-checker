from __future__ import annotations

import re
from typing import Any, Dict, List

from app.models.document_model import (
    DocumentModel,
    FigureModel,
    ParagraphModel,
    ReferenceModel,
    SectionModel,
    TableModel,
)


class DocxParser:
    def parse(self, payload: Dict[str, Any]) -> DocumentModel:
        doc = DocumentModel()

        doc.title = str(payload.get("title", "")).strip()
        doc.english_title = str(payload.get("english_title", "")).strip()
        doc.abstract = str(payload.get("abstract", "")).strip()
        doc.keywords = [str(item).strip() for item in payload.get("keywords", []) if str(item).strip()]

        raw_sections = payload.get("sections", []) or []
        for section in raw_sections:
            doc.sections.append(
                SectionModel(
                    title=str(section.get("title", "")).strip(),
                    level=int(section.get("level", 1) or 1),
                    start_page=section.get("start_page"),
                    end_page=section.get("end_page"),
                )
            )

        raw_paragraphs = payload.get("paragraphs", []) or []
        for idx, paragraph in enumerate(raw_paragraphs, start=1):
            doc.paragraphs.append(
                ParagraphModel(
                    text=str(paragraph.get("text", "")).strip(),
                    font=str(paragraph.get("font", "")).strip(),
                    font_size=str(paragraph.get("font_size", "")).strip(),
                    align=str(paragraph.get("align", "left")).strip() or "left",
                    line_spacing=str(paragraph.get("line_spacing", "1.25")).strip(),
                    section_index=paragraph.get("section_index", idx),
                )
            )

        raw_figures = payload.get("figures", []) or []
        for figure in raw_figures:
            doc.figures.append(
                FigureModel(
                    caption=str(figure.get("caption", "")).strip(),
                    alt_text=str(figure.get("alt_text", "")).strip(),
                    page=figure.get("page"),
                )
            )

        raw_tables = payload.get("tables", []) or []
        for table in raw_tables:
            doc.tables.append(
                TableModel(
                    caption=str(table.get("caption", "")).strip(),
                    page=table.get("page"),
                )
            )

        raw_refs = payload.get("references", []) or []
        for ref in raw_refs:
            if isinstance(ref, dict):
                doc.references.append(
                    ReferenceModel(
                        id=int(ref.get("id", 0) or 0),
                        text=str(ref.get("text", "")).strip(),
                        ref_type=str(ref.get("type", "journal")).strip(),
                    )
                )

        doc.pages = payload.get("pages", {}) or {}
        return doc

    def extract_from_docx(self, file_bytes: bytes) -> DocumentModel:
        # This is the placeholder path for real docx parsing. The system is structured for later integration.
        # In its current state, it accepts a lightweight payload structure instead of raw .docx binary.
        text = file_bytes.decode("utf-8", errors="ignore")
        lines = text.splitlines()

        doc = DocumentModel()
        for line in lines:
            if not line.strip():
                continue
            if re.search(r"[\u4e00-\u9fff]", line) and len(line) < 200:
                doc.sections.append(SectionModel(title=line.strip(), level=1))
            elif "[1]" in line:
                doc.references.append(ReferenceModel(id=1, text=line.strip()))

        doc.pages = {"front_pages": "roman", "main_pages": "arabic"}
        return doc
