from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SectionModel:
    title: str = ""
    level: int = 1
    start_page: Optional[int] = None
    end_page: Optional[int] = None


@dataclass
class ParagraphModel:
    text: str = ""
    font: str = ""
    font_size: str = ""
    align: str = "left"
    line_spacing: str = "1.25"
    section_index: Optional[int] = None


@dataclass
class FigureModel:
    caption: str = ""
    alt_text: str = ""
    page: Optional[int] = None


@dataclass
class TableModel:
    caption: str = ""
    page: Optional[int] = None


@dataclass
class ReferenceModel:
    id: int = 0
    text: str = ""
    ref_type: str = "journal"


@dataclass
class DocumentModel:
    title: str = ""
    english_title: str = ""
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    sections: List[SectionModel] = field(default_factory=list)
    paragraphs: List[ParagraphModel] = field(default_factory=list)
    figures: List[FigureModel] = field(default_factory=list)
    tables: List[TableModel] = field(default_factory=list)
    references: List[ReferenceModel] = field(default_factory=list)
    pages: Dict[str, Any] = field(default_factory=dict)
