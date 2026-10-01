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
        paragraphs = payload.get("paragraphs", []) or []
        pages = payload.get("pages", {}) or {}

        return {
            "title": str(payload.get("title", "")).strip(),
            "english_title": str(payload.get("english_title", "")).strip(),
            "abstract": str(payload.get("abstract", "")).strip(),
            "keywords": payload.get("keywords", []) or [],
            "sections": sections,
            "references": references,
            "figures": figures,
            "tables": tables,
            "paragraphs": paragraphs,
            "pages": pages,
        }


class RuleEngine:
    def __init__(self):
        self.rules = load_rules()
        self.parser = DocumentParser()

    def evaluate(self, payload: Any) -> CheckReport:
        doc = self.parser.parse(payload)
        report = CheckReport()

        # 1. Cover and metadata rules
        if not doc["title"]:
            report.issues.append(self._issue("COVER_TITLE_ALIGNMENT", "Title is missing", "error", "The paper title is required.", "cover", "Add the title on the cover page."))

        if not doc["english_title"]:
            report.issues.append(self._issue("ENGLISH_TITLE_REQUIRED", "English title is missing", "warning", "The English title is required for thesis formatting compliance.", "cover", "Add a proper English title."))

        if 3 <= len(doc["keywords"]) <= 5:
            pass
        elif doc["keywords"]:
            report.issues.append(self._issue("KEYWORDS_COUNT", "Keyword count should be 3-5", "warning", "Keywords should be listed with 3 to 5 entries.", "abstract", "Adjust the keyword count to 3-5 items."))

        # 2. Abstract rules
        if doc["abstract"] and len(doc["abstract"]) < 500:
            report.issues.append(self._issue("ABSTRACT_LENGTH", "Abstract is too short", "warning", "The abstract should be at least 500 Chinese characters long.", "abstract", "Expand the abstract to include purpose, methods, results, and conclusion."))

        # 3. Structure and section rules
        if not doc["sections"]:
            report.issues.append(self._issue("SECTION_LEVELING", "No section structure found", "warning", "The paper should contain chapter and section structure.", "section", "Add chapter headings and subordinate sections."))

        section_titles = [str(s.get("title", "")).strip() for s in doc["sections"]]
        chapter_levels = [int(s.get("level", 1) or 1) for s in doc["sections"]]

        for idx, section in enumerate(doc["sections"], start=1):
            title = str(section.get("title", "")).strip()
            level = int(section.get("level", 1) or 1)
            if level not in {1, 2, 3}:
                report.issues.append(self._issue("SECTION_LEVELING", "Invalid section level", "warning", f"Section '{title}' uses level {level}.", "section", "Adjust the section hierarchy to 1, 2, or 3."))

            if "本章小结" in title and level == 1:
                report.issues.append(self._issue("CHAPTER_SUMMARY", "Summary in the first chapter", "info", "The summary should appear from chapter 2 onward.", "section", "Move or remove the summary section from the first chapter."))

        summary_count = sum(1 for title in section_titles if "本章小结" in title)
        if len(doc["sections"]) >= 3 and summary_count == 0:
            report.issues.append(self._issue("CHAPTER_SUMMARY", "Missing chapter summaries", "warning", "Chapters after the first should include a brief summary section.", "section", "Add a '本章小结' section at the end of each chapter."))

        if "绪论" not in "".join(section_titles):
            report.issues.append(self._issue("CHAPTER_INTRO", "Missing introduction chapter", "warning", "The introduction should be the first chapter in the thesis.", "section", "Add the '绪论' chapter heading as the first chapter."))

        if "总结与展望" not in "".join(section_titles):
            report.issues.append(self._issue("CONCLUSION_SECTION", "Conclusion section is missing", "warning", "The thesis needs a '总结与展望' section before the references.", "section", "Add a separate conclusion section."))

        if "参考文献" not in "".join(section_titles):
            report.issues.append(self._issue("REFERENCES_SECTION", "References section is missing", "warning", "The thesis requires a separate references section.", "section", "Add a '参考文献' section."))

        if "致谢" not in "".join(section_titles):
            report.issues.append(self._issue("ACKNOWLEDGEMENT_SECTION", "Acknowledgements section is missing", "warning", "The thesis should contain an acknowledgements section after the references.", "section", "Add an acknowledgements section."))

        # 4. Page numbering and document structure
        pages = doc["pages"]
        if pages:
            front_pages = pages.get("front_pages")
            main_pages = pages.get("main_pages")
            if front_pages is not None and front_pages != "roman":
                report.issues.append(self._issue("PAGE_NUMBERING_FRONT", "Front matter page numbering is incorrect", "warning", "Abstract and contents pages should use Roman numerals.", "pagination", "Set front matter page numbers to Roman numeral format (I, II, III)."))
            if main_pages is not None and main_pages != "arabic":
                report.issues.append(self._issue("PAGE_NUMBERING_MAIN", "Main text page numbering is incorrect", "warning", "Main body pages should use Arabic numerals.", "pagination", "Set main body page numbers to Arabic numerals."))

        # 5. Figure and table rules
        for figure in doc["figures"]:
            caption = str(figure.get("caption", "")).strip()
            if caption and not caption.startswith("图"):
                report.issues.append(self._issue("FIGURE_CAPTION_FORMAT", "Incorrect figure caption", "error", "Figure captions should start with '图' and use the correct numbering format.", "figure", "Add a caption like '图2-1'."))
            if caption and not re_numeric_pattern(caption):
                report.issues.append(self._issue("FIGURE_CAPTION_FORMAT", "Figure numbering format is invalid", "error", "Figure numbering should follow the chapter format such as '图2-1'.", "figure", "Use the correct chapter-based numbering format."))

        for table in doc["tables"]:
            caption = str(table.get("caption", "")).strip()
            if caption and not caption.startswith("表"):
                report.issues.append(self._issue("TABLE_CAPTION_FORMAT", "Incorrect table caption", "error", "Table captions should start with '表' and use the correct numbering format.", "table", "Add a caption like '表3-1'."))
            if caption and not re_numeric_pattern(caption, prefix="表"):
                report.issues.append(self._issue("TABLE_CAPTION_FORMAT", "Table numbering format is invalid", "error", "Table numbering should follow the chapter format such as '表3-1'.", "table", "Use the correct chapter-based numbering format."))

        # 6. Reference rules
        refs = doc["references"]
        if len(refs) < 15:
            report.issues.append(self._issue("REFERENCE_MIN_COUNT", "Reference count is low", "warning", "The paper should include at least 15 references.", "references", "Expand the reference list to meet the minimum requirement."))

        ids = []
        for ref in refs:
            if isinstance(ref, dict):
                ref_id = ref.get("id")
                if ref_id is not None:
                    try:
                        ids.append(int(ref_id))
                    except (TypeError, ValueError):
                        pass
        if ids and ids != list(range(1, max(ids) + 1)):
            report.issues.append(self._issue("REFERENCE_SEQUENCE", "Reference numbers are not sequential", "error", "Reference numbers should begin at 1 and increase without gaps.", "references", "Renumber the reference list in order."))

        # 7. Paragraph/style rules
        for idx, paragraph in enumerate(doc["paragraphs"], start=1):
            font = str(paragraph.get("font", "")).strip()
            if font and font not in {"宋体", "黑体", "Times New Roman", "Arial", "Calibri"}:
                report.issues.append(self._issue("STYLE_FONT", "Paragraph font is not standard", "warning", f"Paragraph {idx} uses an unusual font name.", "style", "Standardize the font to the thesis specification."))

            if paragraph.get("align") and str(paragraph.get("align", "")).lower() not in {"left", "center", "justify"}:
                report.issues.append(self._issue("STYLE_ALIGNMENT", "Alignment value is not valid", "warning", f"Paragraph {idx} alignment is not in the standard set.", "style", "Use a valid alignment option such as left, center, or justify."))

        # 8. General final counts
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


def re_numeric_pattern(value: str, prefix: str = "图") -> bool:
    import re

    if prefix == "图":
        pattern = r"^图\d+-\d+$"
    else:
        pattern = r"^表\d+-\d+$"

    return bool(re.match(pattern, value.strip()))
