import argparse

from cad_validator.ai import DesignAnomalyDetector
from cad_validator.report import build_report
from cad_validator.rules import run_rule_checks
from cad_validator.sample_data import load_designs_from_json
from cad_validator.scoring import calculate_design_score


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate extracted CAD design features using rules and AI."
    )
    parser.add_argument(
        "--input",
        default="data/sample_designs.json",
        help="Path to a JSON file containing extracted design features.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    designs = load_designs_from_json(args.input)

    detector = DesignAnomalyDetector()
    detector.fit(designs)

    for design in designs:
        issues = run_rule_checks(design)
        ai_prediction = detector.predict(design)
        ai_flagged = ai_prediction == -1
        score = calculate_design_score(issues, ai_flagged)
        report = build_report(design.name, issues, ai_flagged, score)
        print(report)
        print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
