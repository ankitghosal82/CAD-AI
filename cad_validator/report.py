from cad_validator.rules import ValidationIssue
def build_report(design_name:str,issues:list[ValidationIssue],ai_result:dict,score:int)->str:
    status="PASS" if not issues and ai_result["status"]=="PASS" else "NEEDS REVIEW"
    lines = [
        f"Design:{design_name}",
        f"Overall Status:{status}",
        f"Design Score:{score}/100",
        "",
        "--- RULE-BASED CHECKS ---"
    ]
    if not issues:
        lines.append("No deterministic rule violations detected.")
    for issue in issues:
        lines.append(f"{issue.severity}: {issue.message} {issue.suggestion}")
    lines.extend([
        "","--- AI PREDICTION (RANDOM FOREST) ---",f"AI Status: {ai_result['status']} (Confidence:{ai_result['confidence']}%)"
    ])
    if ai_result["insights"]:
        lines.append("Actionable Insights:")
        for insight in ai_result["insights"]:
            lines.append(f" ERROR {insight}")
    return "\n".join(lines)