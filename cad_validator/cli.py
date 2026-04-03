import argparse
from cad_validator.ai import DesignQualityPredictor
from cad_validator.sample_data import load_designs_from_excel
from cad_validator.rules import run_rule_checks
from cad_validator.scoring import calculate_design_score
from cad_validator.report import build_report
from cad_validator.models import DesignFeatures
def main() -> None:
    parser=argparse.ArgumentParser(description="Enterprise CAD Validation Pipeline")
    parser.add_argument("--train",type=str,help="Path to Excel dataset to train the model")
    parser.add_argument("--test",action="store_true",help="Test the AI with a mock bad part")
    args=parser.parse_args()
    predictor=DesignQualityPredictor()
    if args.train:
        designs=load_designs_from_excel(args.train)
        predictor.train(designs)
        predictor.save_model("cad_validator/ai_model.pkl")
    if args.test:
        print("\nLoading pre-trained model for live prediction...")
        predictor.load_model("cad_validator/ai_model.pkl")
        live_part=DesignFeatures("Live_Bracket_01",100.0,50.0,20.0,1.2,10.0,8.0,2,0.0)
        issues=run_rule_checks(live_part)
        ai_result=predictor.predict_with_insights(live_part)
        ai_flagged=ai_result["status"]=="FAIL"
        score=calculate_design_score(issues,ai_flagged)
        report=build_report(live_part.name,issues,ai_result,score)
        print("\n"+"="*60)
        print(report)
        print("="*60)
if __name__ == "__main__":
    main()