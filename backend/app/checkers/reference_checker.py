import re


class ReferenceChecker:
    def check(self, references):
        issues = []
        if len(references) < 15:
            issues.append({
                "rule_id": "REFERENCES_MINIMUM_COUNT",
                "severity": "warning",
                "message": "At least 15 references are recommended.",
            })

        ids = []
        for ref in references:
            if isinstance(ref, dict):
                ref_id = ref.get("id")
                if ref_id is not None:
                    try:
                        ids.append(int(ref_id))
                    except (TypeError, ValueError):
                        pass

        if ids and ids != list(range(1, max(ids) + 1)):
            issues.append({
                "rule_id": "REFERENCE_SEQUENCE",
                "severity": "error",
                "message": "Reference IDs do not begin at 1 and increment sequentially.",
            })

        for ref in references:
            if not isinstance(ref, dict):
                continue
            text = str(ref.get("text", "")).strip()
            if "DOI" in text or "doi" in text:
                issues.append({
                    "rule_id": "DOI_REMOVAL",
                    "severity": "warning",
                    "message": "DOI metadata should be removed from the final bibliography list.",
                })
                break

        return issues
