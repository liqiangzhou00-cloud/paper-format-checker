from __future__ import annotations

from typing import Any, Dict, List

from app.models.document_model import DocumentModel


class DetailedChecker:
    def check_cover(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        if not doc.title:
            issues.append(
                {
                    "rule_id": "COVER_TITLE_ALIGNMENT",
                    "category": "cover",
                    "severity": "error",
                    "title": "论文题目缺失",
                    "message": "封面题目为空。",
                    "location": "cover:title",
                    "page": 1,
                    "suggestion": "在封面填写论文题目，并使用三号黑体居中。",
                    "annotation_id": "1,2,8,12",
                }
            )
        if not doc.english_title:
            issues.append(
                {
                    "rule_id": "ENGLISH_TITLE_REQUIRED",
                    "category": "cover",
                    "severity": "warning",
                    "title": "英文题目缺失",
                    "message": "英文题目为空。",
                    "location": "cover:english_title",
                    "page": 1,
                    "suggestion": "添加英文题目，使用 Times New Roman，首字母大写。",
                    "annotation_id": "9,17",
                }
            )
        return issues

    def check_abstract(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        if not doc.abstract:
            issues.append(
                {
                    "rule_id": "ABSTRACT_LENGTH_CHECK",
                    "category": "abstract",
                    "severity": "warning",
                    "title": "摘要缺失",
                    "message": "中文摘要为空。",
                    "location": "abstract:content",
                    "page": 2,
                    "suggestion": "填写摘要并控制在 500-800 字。",
                    "annotation_id": "14",
                }
            )
        elif len(doc.abstract) < 500:
            issues.append(
                {
                    "rule_id": "ABSTRACT_LENGTH_CHECK",
                    "category": "abstract",
                    "severity": "warning",
                    "title": "摘要过短",
                    "message": f"摘要仅 {len(doc.abstract)} 字，少于 500 字下限。",
                    "location": "abstract:content",
                    "page": 2,
                    "suggestion": "扩展摘要至 500-800 字，覆盖目的、方法、成果、结论。",
                    "annotation_id": "14",
                }
            )

        if not doc.keywords:
            issues.append(
                {
                    "rule_id": "KEYWORDS_COUNT",
                    "category": "abstract",
                    "severity": "warning",
                    "title": "关键词缺失",
                    "message": "关键词为空。",
                    "location": "abstract:keywords",
                    "page": 2,
                    "suggestion": "添加 3-5 个关键词，用中文逗号分隔。",
                    "annotation_id": "15",
                }
            )
        elif not (3 <= len(doc.keywords) <= 5):
            issues.append(
                {
                    "rule_id": "KEYWORDS_COUNT",
                    "category": "abstract",
                    "severity": "warning",
                    "title": "关键词个数不符",
                    "message": f"关键词共 {len(doc.keywords)} 个，应为 3-5 个。",
                    "location": "abstract:keywords",
                    "page": 2,
                    "suggestion": "调整关键词个数到 3-5 个。",
                    "annotation_id": "15",
                }
            )
        return issues

    def check_sections(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        titles = [s.title for s in doc.sections]
        required = {"绪论": "第一章", "总结与展望": "总结与展望", "参考文献": "参考文献", "致谢": "致谢"}
        for key, label in required.items():
            if not any(key in title for title in titles):
                issues.append(
                    {
                        "rule_id": f"MISSING_{key}",
                        "category": "section",
                        "severity": "warning",
                        "title": f"{label}缺失",
                        "message": f"文档中未找到'{key}'章节。",
                        "location": "section:structure",
                        "page": None,
                        "suggestion": f"请添加'{key}'章节。",
                        "annotation_id": "21,47,50,58",
                    }
                )

        for idx, section in enumerate(doc.sections):
            if section.level not in {1, 2, 3}:
                issues.append(
                    {
                        "rule_id": "SECTION_LEVELING",
                        "category": "section",
                        "severity": "warning",
                        "title": "章节层级不规范",
                        "message": f"'{section.title}' 使用了不规范的层级 {section.level}。",
                        "location": f"section:{idx}",
                        "page": section.start_page,
                        "suggestion": "等级调整为 1、2、3。",
                        "annotation_id": "24,25,28",
                    }
                )

        summary_count = sum(1 for title in titles if "本章小结" in title)
        if len(doc.sections) >= 3 and summary_count == 0:
            issues.append(
                {
                    "rule_id": "CHAPTER_SUMMARY_REQUIRED",
                    "category": "section",
                    "severity": "warning",
                    "title": "缺少本章小结",
                    "message": "从第2章起应有'本章小结'部分。",
                    "location": "section:summary",
                    "page": None,
                    "suggestion": "在每章末尾添加'本章小结'，不少于100字。",
                    "annotation_id": "32,33",
                }
            )
        return issues

    def check_references(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        if len(doc.references) < 15:
            issues.append(
                {
                    "rule_id": "REFERENCE_MIN_COUNT",
                    "category": "bibliography",
                    "severity": "warning",
                    "title": "参考文献数量不足",
                    "message": f"参考文献共 {len(doc.references)} 篇，应至少 15 篇。",
                    "location": "references:list",
                    "page": None,
                    "suggestion": "补充参考文献至 15 篇以上。",
                    "annotation_id": "51",
                }
            )

        ids = sorted([ref.id for ref in doc.references if ref.id > 0])
        if ids and ids != list(range(1, max(ids) + 1)):
            issues.append(
                {
                    "rule_id": "REFERENCE_SEQUENCE",
                    "category": "bibliography",
                    "severity": "error",
                    "title": "参考文献编号不连续",
                    "message": f"参考文献编号为 {ids}，不是从 [1] 开始的连续序列。",
                    "location": "references:numbering",
                    "page": None,
                    "suggestion": "重新编排参考文献，确保从 [1] 开始连续编号。",
                    "annotation_id": "27,51",
                }
            )

        for ref in doc.references:
            if "DOI" in ref.text or "doi" in ref.text:
                issues.append(
                    {
                        "rule_id": "DOI_REMOVAL",
                        "category": "bibliography",
                        "severity": "warning",
                        "title": "参考文献包含 DOI",
                        "message": "参考文献中保留了 DOI 元数据。",
                        "location": "references:format",
                        "page": None,
                        "suggestion": "删除 DOI，仅保留必要的引用信息。",
                        "annotation_id": "54",
                    }
                )
                break
        return issues

    def check_figures_tables(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        for idx, figure in enumerate(doc.figures, start=1):
            if figure.caption and not figure.caption.startswith("图"):
                issues.append(
                    {
                        "rule_id": "FIGURE_CAPTION_FORMAT",
                        "category": "figure",
                        "severity": "error",
                        "title": f"第 {idx} 张图题格式错误",
                        "message": f"图题'{figure.caption}'不符合规范。",
                        "location": f"figure:{idx}",
                        "page": figure.page,
                        "suggestion": "确保图题以'图'开头，使用'图 X-X'格式。",
                        "annotation_id": "30",
                    }
                )

        for idx, table in enumerate(doc.tables, start=1):
            if table.caption and not table.caption.startswith("表"):
                issues.append(
                    {
                        "rule_id": "TABLE_CAPTION_FORMAT",
                        "category": "table",
                        "severity": "error",
                        "title": f"第 {idx} 个表题格式错误",
                        "message": f"表题'{table.caption}'不符合规范。",
                        "location": f"table:{idx}",
                        "page": table.page,
                        "suggestion": "确保表题以'表'开头，使用'表 X-X'格式。",
                        "annotation_id": "35",
                    }
                )
        return issues

    def check_styles(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        standard_fonts = {"宋体", "黑体", "Times New Roman", "Arial"}
        for idx, para in enumerate(doc.paragraphs):
            if para.font and para.font not in standard_fonts:
                issues.append(
                    {
                        "rule_id": "STYLE_FONT",
                        "category": "style",
                        "severity": "warning",
                        "title": "字体不规范",
                        "message": f"段落 {idx + 1} 使用了非标准字体 '{para.font}'。",
                        "location": f"paragraph:{idx}",
                        "page": None,
                        "suggestion": "将字体改为宋体、黑体或 Times New Roman。",
                        "annotation_id": "26",
                    }
                )
                break

            if para.line_spacing and para.line_spacing != "1.25":
                issues.append(
                    {
                        "rule_id": "STYLE_LINE_SPACING",
                        "category": "style",
                        "severity": "warning",
                        "title": "行距不规范",
                        "message": f"段落 {idx + 1} 行距为 '{para.line_spacing}'，应为 1.25。",
                        "location": f"paragraph:{idx}",
                        "page": None,
                        "suggestion": "将行距统一设置为 1.25 倍。",
                        "annotation_id": "26",
                    }
                )
                break
        return issues

    def check_pagination(self, doc: DocumentModel) -> List[Dict[str, Any]]:
        issues: List[Dict[str, Any]] = []
        pages = doc.pages or {}
        if pages.get("front_pages") != "roman":
            issues.append(
                {
                    "rule_id": "FRONT_MATTER_PAGE_NUMBER",
                    "category": "pagination",
                    "severity": "error",
                    "title": "摘要页码格式错误",
                    "message": "摘要和目录页码应使用罗马数字。",
                    "location": "pagination:front",
                    "page": 2,
                    "suggestion": "将摘要和目录页码设置为大写罗马数字。",
                    "annotation_id": "16",
                }
            )

        if pages.get("main_pages") != "arabic":
            issues.append(
                {
                    "rule_id": "PAGE_NUMBERING_ARABIC_BODY",
                    "category": "pagination",
                    "severity": "error",
                    "title": "正文页码格式错误",
                    "message": "正文页码应使用阿拉伯数字。",
                    "location": "pagination:main",
                    "page": None,
                    "suggestion": "将正文页码设置为阿拉伯数字。",
                    "annotation_id": "6,16",
                }
            )
        return issues


__all__ = ["DetailedChecker"]
