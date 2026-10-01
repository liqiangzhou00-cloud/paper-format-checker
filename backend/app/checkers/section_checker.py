class SectionChecker:
    def check(self, sections):
        issues = []
        titles = [str(section.get("title", "")).strip() for section in sections]

        for idx, section in enumerate(sections, start=1):
            level = int(section.get("level", 1) or 1)
            title = str(section.get("title", "")).strip()

            if level not in {1, 2, 3}:
                issues.append({
                    "rule_id": "SECTION_LEVELING",
                    "severity": "warning",
                    "message": f"Section {idx} has an invalid heading level: {level}.",
                })

            if "本章小结" in title and level == 1:
                issues.append({
                    "rule_id": "CHAPTER_SUMMARY",
                    "severity": "info",
                    "message": "The chapter summary should not appear in the first chapter.",
                })

        if len(sections) >= 3 and not any("本章小结" in t for t in titles):
            issues.append({
                "rule_id": "CHAPTER_SUMMARY_REQUIRED",
                "severity": "warning",
                "message": "Chapter summaries are missing from the body sections.",
            })

        if not any("绪论" in t for t in titles):
            issues.append({
                "rule_id": "CHAPTER_1_STYLE",
                "severity": "warning",
                "message": "The introduction chapter is missing.",
            })

        if not any("总结与展望" in t for t in titles):
            issues.append({
                "rule_id": "SUMMARY_SECTION",
                "severity": "warning",
                "message": "The conclusion section is missing.",
            })

        if not any("参考文献" in t for t in titles):
            issues.append({
                "rule_id": "BIBLIOGRAPHY_HEADING",
                "severity": "warning",
                "message": "The bibliography section is missing.",
            })

        return issues
