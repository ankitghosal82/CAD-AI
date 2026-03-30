from cad_validator.rules import ValidationIssue


def calculate_design_score(issues: list[ValidationIssue], ai_flagged: bool) -> int:
    score = 100

    for issue in issues:
        if issue.severity == "ERROR":
            score -= 30
        elif issue.severity == "WARNING":
            score -= 15

    if ai_flagged:
        score -= 20

    return max(score, 0)
