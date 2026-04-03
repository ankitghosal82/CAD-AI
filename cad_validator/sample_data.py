import pandas as pd
from pathlib import Path
from cad_validator.models import DesignFeatures
def load_designs_from_excel(file_path: str | Path) -> list[DesignFeatures]:
    print(f"Loading data from {file_path}...")
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df = df.fillna(0) 
    designs = []
    for index, row in df.iterrows():
        design = DesignFeatures(
            name=str(row.get("name", f"Part_{index}")),
            length_mm=float(row.get("length_mm", 0)),
            width_mm=float(row.get("width_mm", 0)),
            height_mm=float(row.get("height_mm", 0)),
            thickness_mm=float(row.get("thickness", row.get("thickness_mm", 0))),
            hole_diameter_mm=float(row.get("hole_diameter", row.get("hole_diameter_mm", 0))),
            hole_edge_distance_mm=float(row.get("hole_edge", row.get("hole_edge_distance_mm", 0))),
            sharp_edge_count=int(row.get("sharp_edge", row.get("sharp_edge_count", 0))),
            fillet_radius_mm=float(row.get("fillet_radius", row.get("fillet_radius_mm", 0))),
            expected_quality=str(row.get("expected_quality", "good")).strip().lower()
        )
        designs.append(design) 
    print(f"Successfully loaded {len(designs)} designs.")
    return designs