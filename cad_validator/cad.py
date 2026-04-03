import FreeCAD as App
import Part
import sys
import os
PROJECT_PATH = "C:\Users\ANKIT\cad-ai\CAD-AI"
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)
from cad_validator.models import DesignFeatures
from cad_validator.rules import run_rule_checks
from cad_validator.ai import DesignQualityPredictor
from cad_validator.scoring import calculate_design_score
from cad_validator.report import build_report
def analyze_active_part():
    doc = App.ActiveDocument
    if not doc:
        print("\n❌ [ERROR] No 3D model is open. Please draw a part first!")
        return
    obj = doc.Objects[0]
    shape = obj.Shape
    print(f"\n🔍 Scanning Geometry for: {obj.Label}...")
    bbox = shape.BoundBox
    length = round(bbox.XMax - bbox.XMin, 2)
    width = round(bbox.YMax - bbox.YMin, 2)
    height = round(bbox.ZMax - bbox.ZMin, 2)
    hole_diameters = []
    for face in shape.Faces:
        if "Cylinder" in str(type(face.Surface)):
            hole_diameters.append(face.Surface.Radius * 2)
    avg_hole_dia = round(sum(hole_diameters) / len(hole_diameters), 2) if hole_diameters else 0.0
    features = DesignFeatures(
        name=obj.Label,
        length_mm=length,
        width_mm=width,
        height_mm=height,
        thickness_mm=height,
        hole_diameter_mm=avg_hole_dia,
        hole_edge_distance_mm=10.0 if avg_hole_dia > 0 else 0.0, 
        sharp_edge_count=len(shape.Edges),
        fillet_radius_mm=0.0
    )
    print(f"📐 Extracted Dimensions: {length}x{width}x{height} mm | Holes Detected: {len(hole_diameters)}")
    issues = run_rule_checks(features)
    predictor = DesignQualityPredictor()
    model_path = os.path.join(PROJECT_PATH, "cad_validator", "ai_model.pkl")
    try:
        predictor.load_model(model_path)
    except FileNotFoundError:
        print(f"\n❌ [CRITICAL ERROR] AI Brain not found at {model_path}.")
        print("Did you run the training command in your terminal first?")
        return
    ai_result = predictor.predict_with_insights(features)
    ai_flagged = ai_result["status"] == "FAIL"
    score = calculate_design_score(issues, ai_flagged)
    final_report = build_report(features.name, issues, ai_result, score)
    print("\n" + "█"*60)
    print("                VARROC AI DESIGN COPILOT")
    print("█"*60)
    print(final_report)
    print("█"*60 + "\n")
analyze_active_part()