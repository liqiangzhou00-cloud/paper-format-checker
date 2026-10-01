class StyleChecker:
    def check(self, paragraphs):
        issues = []
        for idx, paragraph in enumerate(paragraphs, start=1):
            font = str(paragraph.get("font", "")).strip()
            if font and font not in {"宋体", "黑体", "Times New Roman", "Arial", "Calibri"}:
                issues.append({
                    "rule_id": "STYLE_FONT",
                    "severity": "warning",
                    "message": f"Paragraph {idx} uses a nonstandard font name: {font}",
                })

            align = str(paragraph.get("align", "")).lower()
            if align and align not in {"left", "center", "justify"}:
                issues.append({
                    "rule_id": "STYLE_ALIGNMENT",
                    "severity": "warning",
                    "message": f"Paragraph {idx} uses an invalid alignment value: {align}",
                })

        return issues
