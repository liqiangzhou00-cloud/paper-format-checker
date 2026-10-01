class CoverChecker:
    def check(self, title: str, english_title: str, keywords: list[str], abstract: str):
        issues = []

        if not title:
            issues.append({
                "rule_id": "COVER_TITLE_ALIGNMENT",
                "severity": "error",
                "message": "The paper title is missing.",
            })

        if not english_title:
            issues.append({
                "rule_id": "ENGLISH_TITLE_REQUIRED",
                "severity": "warning",
                "message": "The English title is missing.",
            })

        if keywords and not (3 <= len(keywords) <= 5):
            issues.append({
                "rule_id": "KEYWORDS_COUNT",
                "severity": "warning",
                "message": "Keyword count should be between 3 and 5.",
            })

        if abstract and len(abstract) < 500:
            issues.append({
                "rule_id": "ABSTRACT_LENGTH_CHECK",
                "severity": "warning",
                "message": "Abstract length is shorter than the recommended minimum.",
            })

        return issues
