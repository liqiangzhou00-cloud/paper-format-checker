from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Paragraph:
    text: str = ""
    font: str = ""
    font_size: str = ""
    alignment: str = "left"
    line_spacing: str = "1.25"
    first_line_indent: Optional[int] = None
    section_id: Optional[str] = None


@dataclass
class Section:
    title: str = ""
    level: int = 1
    start_page: int = 1
    end_page: int = 1
    text: str = ""


@dataclass
class Figure:
    id: str = ""
    caption: str = ""
    position: str = "center"


@dataclass
class Table:
    id: str = ""
    caption: str = ""
    style: str = ""
    position: str = "center"


@dataclass
class Reference:
    id: int = 0
    text: str = ""
    type: str = "journal"


@dataclass
class Issue:
    rule_id: str
    title: str
    severity: str
    description: str
    location: str = ""
    suggestion: str = ""


@dataclass
class CheckReport:
    summary: Dict[str, int] = field(default_factory=lambda: {"error": 0, "warning": 0, "info": 0})
    issues: List[Issue] = field(default_factory=list)


@dataclass
class CheckRequest:
    title: str = ""
    english_title: str = ""
    abstract: str = ""
    keywords: List[str] = field(default_factory=list)
    sections: List[Dict[str, Any]] = field(default_factory=list)
    references: List[Dict[str, Any]] = field(default_factory=list)
    figures: List[Dict[str, Any]] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    pages: Dict[str, Any] = field(default_factory=dict)
    paragraphs: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class CheckResponse:
    summary: Dict[str, int]
    issues: List[Dict[str, str]]
