from cad_validator.rules import ValidationIssue


def build_report(
    design_name: str,
    issues: list[ValidationIssue],
    ai_flagged: bool,
    score: int,
) -> str:
    status = "PASS" if not issues and not ai_flagged else "NEEDS REVIEW"
    lines = [
        f"Design: {design_name}",
        f"Status: {status}",
        f"Design Score: {score}/100",
        "",
        "Issues:",
    ]

    if not issues and not ai_flagged:
        lines.append("- No rule violations detected.")

    for issue in issues:
        lines.append(f"- {issue.severity}: {issue.message} {issue.suggestion}")

    if ai_flagged:
        lines.append("- AI FLAG: Design pattern is unusual compared with training samples.")

    return "\n".join(lines)
