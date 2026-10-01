class LayoutChecker:
    def check(self, pages=None):
        issues = []
        if not pages:
            return issues

        front_pages = pages.get("front_pages")
        main_pages = pages.get("main_pages")

        if front_pages and front_pages != "roman":
            issues.append({
                "rule_id": "FRONT_MATTER_PAGE_NUMBER",
                "severity": "error",
                "message": "Front matter page numbers must use Roman numerals.",
            })

        if main_pages and main_pages != "arabic":
            issues.append({
                "rule_id": "PAGE_NUMBERING_ARABIC_BODY",
                "severity": "error",
                "message": "The body page numbers must use Arabic numerals.",
            })

        return issues
