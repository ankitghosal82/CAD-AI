from dataclasses import dataclass

from cad_validator.models import DesignFeatures


@dataclass
class ValidationIssue:
    severity: str
    message: str
    suggestion: str


MIN_THICKNESS_MM = 2.0
HOLE_EDGE_DISTANCE_FACTOR = 1.5


def run_rule_checks(design: DesignFeatures) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if design.thickness_mm < MIN_THICKNESS_MM:
        issues.append(
            ValidationIssue(
                severity="WARNING",
                message="Thickness too low.",
                suggestion=f"Increase thickness to at least {MIN_THICKNESS_MM:.1f} mm.",
            )
        )

    min_edge_distance = design.hole_diameter_mm * HOLE_EDGE_DISTANCE_FACTOR
    if design.hole_edge_distance_mm < min_edge_distance:
        issues.append(
            ValidationIssue(
                severity="ERROR",
                message="Hole too close to edge.",
                suggestion="Keep edge distance at least 1.5x hole diameter.",
            )
        )

    if design.sharp_edge_count > 0 and design.fillet_radius_mm <= 0:
        issues.append(
            ValidationIssue(
                severity="WARNING",
                message="Sharp edges detected.",
                suggestion="Add fillet or chamfer where possible.",
            )
        )

    return issues
