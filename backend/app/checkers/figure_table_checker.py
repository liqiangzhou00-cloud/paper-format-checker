import re


class FigureTableChecker:
    def check(self, figures, tables):
        issues = []

        for figure in figures:
            caption = str(figure.get("caption", "")).strip()
            if caption and not caption.startswith("图"):
                issues.append({
                    "rule_id": "FIGURE_CAPTION_FORMAT",
                    "severity": "error",
                    "message": "Figure captions should start with '图'.",
                })
            if caption and not re.match(r"^图\d+-\d+$", caption):
                issues.append({
                    "rule_id": "FIGURE_CAPTION_FORMAT",
                    "severity": "error",
                    "message": "Figure numbers should follow the '图X-X' format.",
                })

        for table in tables:
            caption = str(table.get("caption", "")).strip()
            if caption and not caption.startswith("表"):
                issues.append({
                    "rule_id": "TABLE_CAPTION_FORMAT",
                    "severity": "error",
                    "message": "Table captions should start with '表'.",
                })
            if caption and not re.match(r"^表\d+-\d+$", caption):
                issues.append({
                    "rule_id": "TABLE_CAPTION_FORMAT",
                    "severity": "error",
                    "message": "Table numbers should follow the '表X-X' format.",
                })

        return issues
