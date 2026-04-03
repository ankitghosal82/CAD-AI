from dataclasses import dataclass
@dataclass
class DesignFeatures:
    name:str
    length_mm:float
    width_mm:float
    height_mm:float
    thickness_mm:float
    hole_diameter_mm:float
    hole_edge_distance_mm:float
    sharp_edge_count:int
    fillet_radius_mm:float
    expected_quality:str | None=None
    def to_feature_vector(self) -> list[float]:
        return [
            self.length_mm,
            self.width_mm,
            self.height_mm,
            self.thickness_mm,
            self.hole_diameter_mm,
            self.hole_edge_distance_mm,
            float(self.sharp_edge_count),
            self.fillet_radius_mm,
        ]
    @classmethod
    def get_feature_names(cls)->list[str]:
        return [
            "Length","Width","Height","Thickness","Hole Diameter","Hole Edge Distance","Sharp Edges","Fillet Radius"
        ]